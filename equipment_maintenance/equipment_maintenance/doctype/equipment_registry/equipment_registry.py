# Copyright (c) 2025, sathwik and contributors
# For license information, please see license.txt
from __future__ import annotations
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, add_months, getdate, today


class EquipmentRegistry(Document):
    """Controller for Equipment Registry"""

    def after_insert(self):
        """
        Triggered automatically after a new Equipment Registry record is created.
        This will schedule preventive Maintenance Work Orders.
        """
        try:
            frappe.logger().info(f"[AutoSchedule] after_insert for {self.name}")
            schedule_preventive_work_orders(self.name)
        except Exception:
            frappe.log_error("Auto-scheduling MWOs failed", frappe.get_traceback())

def _add_interval(start, frequency: str, cycle_no: int):
    """
    Return the next due date based on frequency string and cycle number.
    """
    if frequency == "Daily":
        return add_days(start, cycle_no * 1)
    if frequency == "Weekly":
        return add_days(start, cycle_no * 7)
    if frequency == "Monthly":
        return add_months(start, cycle_no * 1)
    if frequency == "Quarterly":
        return add_months(start, cycle_no * 3)
    if frequency == "Yearly":
        return add_months(start, cycle_no * 12)
    return None


def _get_checklist_rows_with_frequency(equipment_type: str) -> list[dict]:
    
    if not equipment_type:
        return []

    return frappe.get_all(
        "Standard Maintenance Checklist Item",           
        filters={
            "parentfield": "standard_maintenance_checklist_table_with_checkpoints",  # <-- parent table fieldname
        },
        fields=["checkpoint", "description", "frequency"],
        order_by="idx asc",
    )


def _mwo_exists(equipment: str, scheduled_date, task_description: str) -> bool:
    """
    Check if a Maintenance Work Order already exists for the same equipment,
    due date and task description.
    """
    return bool(
        frappe.db.exists(
            "Maintenance Work Order",
            {
                "equipment": equipment,
                "work_order_type": "Preventive",
                "scheduled_date": getdate(scheduled_date),
                "description": task_description,
            },
        )
    )
@frappe.whitelist()
def schedule_preventive_work_orders(equipment_name: str):
    """
    Generate preventive Maintenance Work Orders for a given Equipment Registry
    based on each checklist row's frequency.
    """
    eq = frappe.get_doc("Equipment Registry", equipment_name)

    # Safety check
    if (eq.status or "").strip().lower() == "decommissioned":
        frappe.msgprint(f"Skipping: {eq.name} is Decommissioned.")
        frappe.logger().info(f"[AutoSchedule] skip decommissioned {equipment_name}")
        return

    start_date = getdate(eq.installation_date) if eq.installation_date else getdate(today())
    checklist_items = _get_checklist_rows_with_frequency(eq.equipment_type)

    if not checklist_items:
        frappe.msgprint(f"No checklist items with frequency for Equipment Type {eq.equipment_type}")
        frappe.logger().info(f"[AutoSchedule] no checklist rows for {equipment_name}")
        return

    first_due_overall = None
    total_created = 0
    cycles = 4   # create 4 future occurrences for each checklist row

    for item in checklist_items:
        frequency = (item.get("frequency") or "").strip()
        if not frequency:
            frappe.logger().info(f"[AutoSchedule] skip {item.checkpoint} (no frequency)")
            continue

        task_description = item.get("checkpoint") or item.get("description") or "Checklist Task"

        for k in range(1, cycles + 1):
            due_date = _add_interval(start_date, frequency, k)
            if not due_date:
                continue

            # Avoid duplicates
            if _mwo_exists(eq.name, due_date, task_description):
                frappe.logger().info(f"[AutoSchedule] exists {task_description} {due_date}")
                continue

            # Create the Maintenance Work Order
            mwo = frappe.new_doc("Maintenance Work Order")
            mwo.update({
                "work_order_type": "Preventive",
                "equipment": eq.name,
                "scheduled_date": due_date,
                "status": "Scheduled",
                "priority": "Medium",
                "assigned_technician": eq.assigned_technician,
                "description": f"{task_description} ({frequency})",
            })

            # Add the task row inside MWO
            mwo.append("maintenance_tasks", {
                "task_description": task_description,
                "is_completed": 0
            })

            mwo.insert(ignore_permissions=True)
            frappe.logger().info(f"[AutoSchedule] created MWO {mwo.name} for {task_description}")
            total_created += 1

            if not first_due_overall or due_date < first_due_overall:
                first_due_overall = due_date

    # Update next_maintenance_due on the Equipment Registry
    if first_due_overall:
        eq.db_set("next_maintenance_due", getdate(first_due_overall))

    frappe.msgprint(f"Auto-scheduling: created {total_created} preventive MWO(s) for {eq.name}.")
    frappe.logger().info(f"[AutoSchedule] finish {equipment_name} created={total_created}")


# -------------------------------------------------------------------
# Hook entry point (if using hooks.py)
# -------------------------------------------------------------------

def after_insert_handler(doc, method=None):
    """
    Hook function so that hooks.py can call it.
    """
    try:
        frappe.logger().info(f"[AutoSchedule] hook after_insert for {doc.name}")
        schedule_preventive_work_orders(doc.name)
    except Exception:
        frappe.log_error("Auto-scheduling MWOs failed (hook)", frappe.get_traceback())

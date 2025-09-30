
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class MaintenanceWorkOrder(Document):
	pass
    # def validate(self):
    #     equipment_status = frappe.db.get_value("Equipment Registry", self.equipment, "status")
    #     if equipment_status == "Decommissioned":
    #         frappe.throw("Cannot create Work Order for Decommissioned Equipment.")

    # def before_save(self):
    #     total_parts_cost = 0
    #     for part in self.parts_used:
    #         total_parts_cost += part.qty * part.rate

    #     technician_hourly_rate = 500 
    #     total_labor_cost = self.labor_hours * technician_hourly_rate

    #     self.total_cost = total_parts_cost + total_labor_cost

    # def on_submit(self):

    #     equipment = frappe.get_doc("Equipment Registry", self.equipment)
    #     if self.status == "In Progress":
    #         equipment.status = "Under Maintenance"
    #     elif self.status == "Completed":
    #         equipment.status = "Active"
    #         equipment.last_maintenance_date = get_datetime(self.completion_date).date()
          
    #     equipment.save()

    #       if self.assigned_technician:
    #         technician_email = frappe.db.get_value("Employee", self.assigned_technician, "company_email")
    #         if technician_email:
    #             frappe.sendmail(
    #                 recipients=technician_email,
    #                 subject=f"New Work Order Assigned: {self.name}",
    #                 message=f"You have been assigned a new maintenance work order {self.name} for {self.equipment}."
    #             )
# Equipment Maintenance Management System
## Technical Assessment Project

### Overview
You are tasked with developing an Equipment Maintenance Management System that integrates with ERPNext. This system will help organizations track their equipment, schedule maintenance activities, and manage work orders.

### Project Duration: 3-4 Days

---

## Requirements

### Part 1: Frappe Backend Development (40% of evaluation)

#### 1.1 Custom DocTypes
Create the following custom DocTypes with appropriate fields and relationships:

**Equipment Registry**
- Equipment ID (auto-generated with series EQP-YYYY-####)
- Equipment Name
- Equipment Type (Link to Equipment Type master)
- Asset (Link to ERPNext Asset)
- Location
- Installation Date
- Warranty Expiry Date
- Status (Active, Under Maintenance, Decommissioned)
- Last Maintenance Date
- Next Maintenance Due
- Assigned Technician (Link to Employee)

**Equipment Type**
- Type Name
- Description
- Maintenance Frequency (in days)
- Standard Maintenance Checklist (Table with checkpoints)

**Maintenance Work Order**
- Work Order ID (auto-generated with series MWO-YYYY-####)
- Equipment (Link to Equipment Registry)
- Work Order Type (Preventive, Corrective, Emergency)
- Scheduled Date
- Completion Date
- Assigned Technician (Link to Employee)
- Status (Draft, Scheduled, In Progress, Completed, Cancelled)
- Priority (Low, Medium, High, Critical)
- Description
- Maintenance Tasks (Table with task descriptions and completion status)
- Parts Used (Table linking to ERPNext Items)
- Labor Hours
- Total Cost
- Completion Notes

#### 1.2 Server Scripts and Automation
Implement the following server-side logic:

1. **Auto-scheduling**: When equipment is created, automatically create preventive maintenance work orders based on equipment type frequency
2. **Status Updates**: Update equipment status when work orders are created/completed
3. **Cost Calculation**: Auto-calculate total maintenance cost from parts and labor
4. **Notifications**: Send email notifications to technicians when work orders are assigned
5. **Validation**: Prevent scheduling maintenance on decommissioned equipment

#### 1.3 Custom API Endpoints
Create REST API endpoints for:
- `/api/method/maintenance.api.get_dashboard_data` - Returns maintenance statistics
- `/api/method/maintenance.api.get_equipment_history` - Returns maintenance history for equipment
- `/api/method/maintenance.api.update_work_order_status` - Updates work order status from mobile interface

### Part 2: ERPNext Integration (30% of evaluation)

#### 2.1 Core Module Integration
- Link Equipment Registry with ERPNext Asset module
- Create Material Requests automatically when maintenance requires parts
- Generate Purchase Orders for maintenance supplies
- Track maintenance costs in Project Costing
- Integrate with Employee master for technician assignment

#### 2.2 Workflows
Implement approval workflows for:
- High-value maintenance work orders (>$1000)
- Emergency maintenance requests
- Equipment decommissioning

#### 2.3 Custom Reports
Create the following reports:
- Equipment Maintenance Schedule (shows upcoming maintenance)
- Maintenance Cost Analysis (by equipment, type, period)
- Technician Workload Report
- Equipment Downtime Analysis

### Part 3: React Frontend (30% of evaluation)

#### 3.1 Maintenance Technician Dashboard
Build a React-based web application with the following features:

**Dashboard Components:**
- Today's assigned work orders
- Equipment status overview (pie chart)
- Recent maintenance activities timeline
- Upcoming scheduled maintenance

**Work Order Management:**
- List view of assigned work orders with filtering and sorting
- Detailed work order view with task checklist
- Mobile-friendly interface for field technicians
- Photo upload for before/after maintenance
- Parts consumption tracking

**Equipment Search and History:**
- Equipment search with QR code scanning capability
- Equipment maintenance history view
- Equipment location mapping (if location coordinates available)

#### 3.2 Technical Requirements
- Use modern React (Hooks, Context API)
- Implement responsive design (mobile-first)
- Use Frappe's REST API for data operations
- Implement proper error handling and loading states
- Add offline capability for field technicians
- Use a modern UI library (Material-UI, Ant Design, or Chakra UI)

---

## Submission Requirements

### 1. GitHub Repository Structure
```
equipment-maintenance-system/
├── README.md
├── frappe_app/
│   ├── maintenance/
│   │   ├── doctype/
│   │   ├── api/
│   │   ├── hooks.py
│   │   └── modules.txt
│   └── setup.py
├── react_frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── docs/
│   ├── installation.md
│   ├── api_documentation.md
│   └── user_guide.md
└── demo_data/
    └── sample_data.json
```

### 2. Documentation Requirements
Include comprehensive documentation covering:
- Installation and setup instructions
- API documentation with examples
- User guide with screenshots
- Database schema documentation
- Known limitations and future enhancements

### 3. Code Quality Standards
- Follow Frappe development best practices
- Implement proper error handling
- Add appropriate comments and docstrings
- Include unit tests for critical functions
- Follow React best practices and patterns

### 4. Demo Data
Provide sample data including:
- 10+ equipment records
- 5+ equipment types
- 20+ maintenance work orders
- Sample maintenance checklists

---

## Evaluation Criteria

### Frappe Development (40%)
- DocType design and relationships (10%)
- Server scripts and automation (10%)
- API implementation (10%)
- Code quality and best practices (10%)

### ERPNext Knowledge (30%)
- Integration with core modules (15%)
- Understanding of business processes (10%)
- Workflow implementation (5%)

### React Skills (30%)
- Component design and architecture (10%)
- UI/UX implementation (10%)
- API integration and state management (10%)

---

## Submission Instructions

### 1. GitHub Repository
- Create a public GitHub repository
- Ensure all code is committed with meaningful commit messages
- Include a comprehensive README.md with setup instructions
- Tag the final submission as `v1.0.0`

### 2. Email Submission
Send an email to `hr@unityedu.ai` with the subject line: `Technical Assessment Submission - [Your Name]`

Include:
- Link to your GitHub repository
- Brief summary of implemented features
- Any assumptions or design decisions made
- Time spent on each part of the project
- Link to screencast video

### 3. Screencast Video
Record a 10-15 minute screencast demonstration using tools like:
- Komodo (recommended)
- Loom

**Video should demonstrate:**
- System setup and installation
- Key features working end-to-end
- Both backend and frontend functionality
- Code walkthrough of key components
- Any challenges faced and how you solved them

---

## Bonus Points
- Implement mobile-responsive design
- Add real-time notifications using Socket.IO
- Implement advanced search and filtering
- Add data visualization charts
- Include automated testing
- Deploy the application (with instructions)
- Implement role-based permissions

---

## Resources
- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [ERPNext Developer Documentation](https://docs.erpnext.com/)
- [React Documentation](https://react.dev/)

**Note**: Focus on demonstrating your understanding of each technology stack rather than building a production-ready system. Quality over quantity is preferred.

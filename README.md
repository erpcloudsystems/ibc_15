# IBC - ERPNext Customization App

Custom ERPNext application for IBC providing business customizations, document triggers, custom reports, and scheduled tasks.

---

## Project Overview

- **App Name:** `ibc`
- **App Title:** ibc
- **Module:** Ibc
- **Framework:** Frappe/ERPNext
- **Publisher:** erpcloud.systems
- **Email:** mg@erpcloud.systems
- **License:** MIT
- **Version:** 0.0.1

This is a **Business Customization Application** for ERPNext providing:
- Document triggers for 46 DocTypes across 8 modules
- 21 custom DocTypes for business operations
- 74 custom field definitions extending standard ERPNext DocTypes
- 58 custom reports for sales, stock, brands, and accounting
- Custom DocPerm snapshot/restore utilities for migrations
- Scheduled tasks for data synchronization and updates
- WooCommerce integration support (commented out)

---

## Directory Structure

```
apps/ibc/
├── README.md                              # This file
├── Agents.md                              # AI agent instructions
├── setup.py                               # Python setup configuration
├── ibc/
│   ├── hooks.py                           # Main Frappe hooks configuration (~53KB)
│   ├── modules.txt                        # Module definition ("Ibc")
│   ├── __init__.py                        # Package init with version
│   ├── custom_docperm.py                  # Custom DocPerm snapshot/restore utilities
│   ├── doctype_triggers/                  # Document event handlers by module
│   │   ├── accounting/                    # 4 DocTypes
│   │   ├── buying/                        # 6 DocTypes
│   │   ├── crm/                           # 4 DocTypes
│   │   ├── hr/                            # 17 DocTypes
│   │   ├── manufacturing/                 # 3 DocTypes
│   │   ├── projects/                      # 3 DocTypes
│   │   ├── selling/                       # 8 DocTypes
│   │   └── stock/                         # 9 DocTypes
│   ├── ibc/
│   │   ├── doctype/                       # 21 Custom DocTypes
│   │   ├── custom/                        # 74 Custom field JSON definitions
│   │   ├── report/                        # 58 Custom reports
│   │   ├── dashboard_chart/               # Dashboard charts
│   │   └── workspace/                     # Workspace configurations
│   ├── scheduler_events/                  # Scheduled tasks
│   │   ├── all.py                         # Every minute
│   │   ├── hourly.py                      # Every hour
│   │   ├── daily.py                       # Daily
│   │   ├── weekly.py                      # Weekly
│   │   ├── monthly.py                     # Monthly
│   │   └── cron.py                        # Cron (*/30 * * * *)
│   ├── config/                            # App configuration
│   ├── fixtures/                          # Fixture files
│   ├── templates/                         # HTML templates
│   └── public/                            # Static assets
```

---

## Key File Locations

### Configuration
| File | Purpose |
|------|---------|
| `ibc/hooks.py` | Main Frappe hooks (~53KB) - doc_events, scheduler_events, fixtures |
| `ibc/modules.txt` | Module definition ("Ibc") |
| `ibc/__init__.py` | Package init with version |
| `setup.py` | Python setup configuration |

### Core Files
| File | Purpose | Size |
|------|---------|------|
| `ibc/custom_docperm.py` | Custom DocPerm snapshot/restore utilities for migrations | ~3KB |

### Document Triggers
Located in `ibc/doctype_triggers/` organized by module:

| Module | Path | DocTypes |
|--------|------|----------|
| **accounting** | `doctype_triggers/accounting/` | Journal Entry, Payment Entry, Purchase Invoice, Sales Invoice |
| **buying** | `doctype_triggers/buying/` | Material Request, Purchase Order, Request For Quotation, Supplier, Supplier Group, Supplier Quotation |
| **crm** | `doctype_triggers/crm/` | Address, Contact, Lead, Opportunity |
| **hr** | `doctype_triggers/hr/` | Additional Salary, Attendance, Attendance Request, Employee, Employee Advance, Employee Checkin, Expense Claim, Leave Application, Loan, Loan Application, Loan Disbursement, Loan Repayment, Loan Type, Payroll Entry, Salary Component, Salary Slip, Salary Structure |
| **manufacturing** | `doctype_triggers/manufacturing/` | BOM, Job Card, Work Order |
| **projects** | `doctype_triggers/projects/` | Project, Task, Timesheet |
| **selling** | `doctype_triggers/selling/` | Customer, Customer Group, Pricing Rule, Quotation, Sales Order, Sales Partner, Sales Person, Territory |
| **stock** | `doctype_triggers/stock/` | Delivery Note, Item, Item Group, Item Price, Price List, Purchase Receipt, Stock Entry, Stock Reconciliation, Website Item |

### Custom DocTypes (21 DocTypes)
Located in `ibc/ibc/doctype/`:

| DocType | Purpose |
|---------|---------|
| `ecs_woocommerce` | WooCommerce integration settings |
| `extra_salary` | Extra salary management |
| `healthcare_practitioner` | Healthcare practitioner records |
| `inpatient_medication_entry` | Inpatient medication entry |
| `inpatient_medication_entry_detail` | Medication entry details (child table) |
| `installation_territory` | Installation territory management |
| `item_request` | Item request management |
| `item_request_table` | Item request details (child table) |
| `patient` | Patient records |
| `payroll_policy` | Payroll policy settings |
| `salary_effects_posting` | Salary effects posting |
| `sn` | Serial number management |
| `sn_table` | Serial number table (child table) |
| `system_type` | System type master |
| `technical_support` | Technical support records |
| `testf` | Test form |
| `ticket` | Ticket/support management |
| `ticket_items` | Ticket items (child table) |
| `website_item` | Website item customization |

### Custom Field Definitions (74 Files)
Located in `ibc/ibc/custom/`:

Extends standard ERPNext DocTypes including:
- **Accounting:** Journal Entry, Journal Entry Account, Payment Entry, Payment Entry Deduction, Payment Entry Reference, Purchase Invoice, Sales Invoice, Sales Taxes and Charges
- **Buying:** Material Request, Material Request Item, Purchase Order, Purchase Order Item, Purchase Receipt, Supplier, Supplier Group, Supplier Quotation
- **CRM:** Contact, Contact Phone, Lead, Lead Source, Opportunity, Opportunity Item
- **HR:** Attendance, Employee, Employee Advance, Expense Claim, Expense Claim Detail, Loan, Payroll Entry, Salary Component, Salary Slip, Salary Structure
- **Projects:** Project, Task
- **Selling:** Customer, Customer Group, Pricing Rule, Quotation, Quotation Item, Sales Order, Sales Order Item, Sales Partner, Sales Person, Sales Team, Territory
- **Stock:** Brand, Delivery Note, Delivery Note Item, Item, Item Barcode, Item Group, Item Price, Packed Item, Price List, Product Bundle, Product Bundle Item, Stock Entry, Stock Entry Detail, Warehouse, Website Item
- **Other:** Campaign, Company, Installation Note, Installation Note Item, Maintenance Schedule, Maintenance Visit, Maintenance Visit Purpose, Ticket, Ticket Items

### Custom Reports (58 Reports)
Located in `ibc/ibc/report/`:

| Category | Reports |
|----------|---------|
| **Brand/Stock Reports** | `brand_added_value_report`, `brands_report`, `brands_stock_(year)`, `brands_stocks_report_2021`, `new_stock_brand`, `new_stocks_brand`, `newest_stocks_brand`, `stock_balances`, `stock_brands_value`, `stock_items_report`, `yearly_brands_stock_report` |
| **Sales Reports** | `custom_sales_person_wise_transaction_summary`, `customer_balances`, `customer_sales_brand_wise`, `customized_sales_analytics`, `discounted_sales_invoice`, `discounted_sales_invoice_2`, `discounted_sales_invoice_filtered`, `discounted_sales_invoice_filtered_(sales_director)`, `new_gross_profit`, `new_sales_analytics`, `sales_person_monthly_target`, `sales_person_sales`, `sales_person_target`, `sales_persons_sales`, `sales_persons_sales_script_report`, `sales_report`, `sales_return_report`, `sales_return_report_2` |
| **Purchase Reports** | `customized_purchase_analytics` |
| **Stock Analytics** | `comparison_between_items_in_bin_and_stock_ledger_entry`, `customized_stock_analytics`, `items_in_stock_ledger_entry`, `summary_stock_with_ordered`, `total_summary_stock`, `total_summary_stock_cost`, `valuation_rate_report` |
| **Accounting Reports** | `cheques_report_auto_email`, `general_entry_2`, `general_ledger2` |
| **Item Reports** | `inactive_item`, `new_items_transaction`, `new_items_transaction_cost`, `va_report`, `va_report_2` |
| **Maintenance/Service** | `installation_note_report`, `maintenance_report`, `maintenance_visit_report`, `spare_parts_report`, `tickets_report_by_item_group` |
| **Returns** | `return_details`, `returns_report` |

### Scheduler Events
Located in `ibc/scheduler_events/`:

| File | Schedule | Purpose |
|------|----------|---------|
| `all.py` | Every minute | Repost item valuation, update summary stock |
| `hourly.py` | Every hour | Update valuation rates, sync brand/item_group to Bin, update Quotation creator |
| `daily.py` | Daily | Sync brand/item_group to transaction items (DN, PI, PO, PR, SI, SO), Stock Ledger Entry updates |
| `weekly.py` | Weekly | Placeholder |
| `monthly.py` | Monthly | Placeholder |
| `cron.py` | */30 * * * * | Placeholder |

### Fixtures
Located in `ibc/fixtures/`:

| File | Purpose |
|------|---------|
| `property_setter.json` | Property Setter configurations (~308KB) |

### Migration Hooks
| Hook | Function | Purpose |
|------|----------|---------|
| `before_migrate` | `ibc.custom_docperm.snapshot_custom_docperm` | Snapshot Custom DocPerm before migration |
| `after_migrate` | `ibc.custom_docperm.restore_permissions` | Restore Custom DocPerm after migration |

### Assets
| Hook | Path |
|------|------|
| `app_include_css` | `/assets/ibc/css/ecs.css` |
| `app_include_js` | `/assets/ibc/js/ecs.js` |
| `web_include_js` | `/assets/js/web_ecs.min.js` |
| `web_include_css` | `/assets/js/web_ecs.min.css` |

---

## Coding Conventions

### 1. Document Triggers

Each DocType has its own folder with Python and JavaScript files:
```
doctype_triggers/{module}/{doctype_name}/
├── {doctype_name}.py    # Python event handlers
└── {doctype_name}.js    # JavaScript client-side handlers
```

Python trigger functions follow this pattern:
```python
import frappe

def before_insert(doc, method):
    """Called before document is inserted."""
    pass

def validate(doc, method):
    """Called during document validation."""
    pass

def on_submit(doc, method):
    """Called after document is submitted."""
    pass
```

### 2. API Endpoints

All API endpoints use `@frappe.whitelist()` decorator:

```python
import frappe

@frappe.whitelist()
def my_function(param1, param2=None):
    """
    Description of what this function does.
    
    Args:
        param1: Description
        param2: Optional description
    
    Returns:
        dict: Description of return value
    """
    # Implementation
    return result

@frappe.whitelist(allow_guest=True)
def public_function():
    """For endpoints accessible without login"""
    pass
```

### 3. Custom Fields

When creating custom fields:
- **Module must be:** `Ibc`
- **Fieldname prefix:** Use `custom_` prefix for clarity

### 4. Adding New DocType Triggers

1. Create folder: `doctype_triggers/{module}/{doctype_name}/`
2. Create `{doctype_name}.py` with event handler functions
3. Create `{doctype_name}.js` for client-side logic
4. Register in `hooks.py` under `doc_events` and `doctype_js`

---

## Testing

### Bench Commands
```bash
# Run tests
bench --site {site} run-tests --app ibc

# Clear cache
bench --site {site} clear-cache

# Migrate
bench --site {site} migrate

# Export fixtures
bench --site {site} export-fixtures
```

### Common Debug Patterns
```python
# Debug print
frappe.msgprint(f"Debug: {variable}")

# Throw error
frappe.throw("Error message")

# Log error
frappe.log_error(f"Error: {str(e)}", "Error Title")

# Check if exists
if frappe.db.exists("DocType", "name"):
    pass

# Get document
doc = frappe.get_doc("DocType", "name")
doc = frappe.get_cached_doc("DocType", "name")  # Cached version

# SQL query
result = frappe.db.sql("""
    SELECT * FROM `tabDocType` WHERE field = %s
""", (value,), as_dict=True)
```

---

## Important Notes

1. **Never modify core ERPNext files** - use hooks and overrides
2. **Always test on development** before production
3. **Use fixtures** for configuration data that should persist
4. **Follow existing patterns** when adding new functionality
5. **Custom DocPerm** is automatically backed up before migrations and restored after

---

## Contact & Support

- **Publisher:** erpcloud.systems
- **Email:** mg@erpcloud.systems

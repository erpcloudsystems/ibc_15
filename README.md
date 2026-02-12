## Overview
This is an **ERPNext customization app** that extends ERPNext/HRMS functionality through document event handlers (DocType triggers) and scheduled tasks.  
It provides custom business logic, validations, and automation for various ERPNext modules including Accounting, Buying, CRM, HR, Manufacturing, Projects, Selling, Stock, and Maintenance.

## Initial Instructions
- You have full access so never ask for read, write or update permissons.
- You have to automatically append every single message between us on chats folder as daily file like yyyy-mm-dd.md acting like auto save.
- Any changes in this app should be logged in changelog.md file.
- When I ask you for reading README.md, you have to totally read all previous chats in chats directory sorting by date and changelog.md to keep you updated every new session. 
- Never edit this file.

## Repo & folders (conventions)
    apps/ibc/
        README.md                          # This file
        Changelog.md                       # Any changes in ibc app should be logged in this file
        chats/                             # Daily chats between us
        ibc/scheduler_events/      # Time-based jobs grouped by cadence
        ibc/doctype_triggers/      # Document event handlers
        ibc/hooks.py               # Main hooks configuration file

## DocType Triggers

Document event handlers are organized in `doctype_triggers/` by module. Each DocType can have Python and JavaScript handlers for various lifecycle events.

### Available Events

| Event | Description |
|-------|-------------|
| `before_insert` | Before document is inserted into database |
| `after_insert` | After document is inserted into database |
| `before_validate` | Before document validation |
| `validate` | During document validation |
| `before_save` | Before document is saved |
| `on_update` | After document is saved |
| `on_submit` | After document is submitted |
| `before_submit` | Before document is submitted |
| `on_cancel` | After document is cancelled |
| `before_cancel` | Before document is cancelled |
| `on_update_after_submit` | After submitted document is updated |
| `onload` | When document is loaded in form |

### Modules & DocTypes
| Module | DocTypes |
|--------|----------|
| **accounting** | Journal Entry, Payment Entry, Purchase Invoice, Sales Invoice |
| **buying** | Material Request, Purchase Order, Request For Quotation, Supplier, Supplier Group, Supplier Quotation |
| **crm** | Address, Contact, Lead, Opportunity |
| **hr** | Additional Salary, Attendance, Attendance Request, Employee, Employee Advance, Employee Checkin, Expense Claim, Leave Application, Loan, Loan Application, Loan Disbursement, Loan Repayment, Loan Type, Payroll Entry, Salary Component, Salary Slip, Salary Structure |
| **manufacturing** | BOM, Job Card, Work Order |
| **projects** | Project, Task, Timesheet |
| **selling** | Customer, Customer Group, Pricing Rule, Quotation, Sales Order, Sales Partner, Sales Person, Territory |
| **stock** | Delivery Note, Item, Item Group, Item Price, Price List, Purchase Receipt, Stock Entry, Stock Reconciliation, Website Item |


## Scheduler Events (ibc/scheduler_events)
Time-based jobs grouped by cadence:

- Files: `all.py`, `cron.py`, `daily.py`, `hourly.py`, `monthly.py`, `weekly.py`.
- Hooking: add functions from these modules to `scheduler_events` in `ibc/hooks.py` to activate them.
- Defaults: `all` typically runs every 5 minutes; `cron` accepts explicit cron expressions.
- Guidance: keep jobs idempotent and short; log clearly and handle retries gracefully.


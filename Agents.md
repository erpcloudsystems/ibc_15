# Agents.md — IBC (ERPNext v15)

Owner: ERP Cloud Systems  
Target Site: ibc.erpnext.cloud  
Stack: ERPNext v15 + custom app `ibc` (backend API + fixtures) + frontend  

---

## 🔴 Critical Agent Rules (Read First)

1. The agent must **automatically append every chat message** into:


chats/YYYY-MM-DD.md


- Acts as auto-save
- Messages must be appended in order
2. When asked to **read `Agents.md`**, the agent must:
- Read **all chat files**
- Sort by date
- Fully hydrate context before responding
3. The agent must **automatically update `Changelog.md`** on **every change**
4. **NEVER edit this file (`Agents.md`)**
5. The agent has **full access** — never ask for read/write/update permissions
6. **Before creating any `.py`, `.js`, `.json`:**
- Ask first to create the **Doctype / Child Table as blank** in ERPNext
7. **Standard DocType customizations**
- Must be done via **fixtures**
- Never modify core files directly

---

## 📦 Repository Structure (Canonical)



apps/ibc/
│
├── Agents.md
├── Changelog.md
├── README.md
│
├── chats/
│   └── YYYY-MM-DD.md
│
├── ibc/
│   │
│   ├── doctype_triggers/      # Document event handlers by module
│   │   ├── accounting/
│   │   ├── buying/
│   │   ├── crm/
│   │   ├── hr/
│   │   ├── manufacturing/
│   │   ├── projects/
│   │   ├── selling/
│   │   └── stock/
│   │
│   ├── scheduler_events/      # Time-based jobs grouped by cadence
│   ├── hooks.py               # Main hooks configuration
│   ├── config/
│   ├── fixtures/
│   ├── public/
│   ├── templates/
│   └── www/



---

## 🧠 Doctype Triggers

**Path**


ibc/doctype_triggers/<module>/<doctype>/<doctype>.py
ibc/doctype_triggers/<module>/<doctype>/<doctype>.js

`

**Supported Events**
- before_insert
- after_insert
- onload
- before_validate
- validate
- before_save
- on_submit
- on_cancel
- before_cancel
- on_update
- on_update_after_submit

**hooks.py**
```python
doc_events = {
    "Sales Invoice": {
        "before_save": "ibc.doctype_triggers.accounting.sales_invoice.sales_invoice.before_save"
    },
    "Delivery Note": {
        "onload": "ibc.doctype_triggers.stock.delivery_note.delivery_note.onload"
    }
}
```

---

## ⏱ Scheduler Events

**Location**


ibc/scheduler_events/ (all.py, cron.py, daily.py, hourly.py, monthly.py, weekly.py)


**Cadences**

* all          (every 5 minutes)
* hourly
* daily
* weekly
* monthly
* cron         (explicit expressions)

**Rules**

* Idempotent
* Short execution
* Logged clearly
* Retry safe

---

## 🚀 Performance Rules (Mandatory)

### Database

* ❌ frappe.db.get_value
* ✅ frappe.db.get_cached_value

### Bulk Reads

* ❌ Queries inside loops
* ✅ frappe.get_all / frappe.get_list

### Child Tables

* Avoid append in loops
* Build list then extend

### Client Scripts

* Minimize frm.refresh()
* Avoid render loops

### Background Jobs

* Heavy logic → enqueue
* UI logic → lightweight only

---

## 📊 Performance Reporting (Internal)

**Location**


ibc/performance/ (if needed)


**Files**

* performance_log.md
* query_changes.md
* optimization_summary.md

Tracks:

* Cached value replacements
* Query count reductions
* Hook optimizations
* Load-time improvements

---

## 🧩 Custom Fields (Fixtures Only)

**Structure**


ibc/fixtures/custom_field.json


**hooks.py**

```python
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["module", "ibc"]
        ]
    }
]
```

**Rules**

* Module must always be `ibc`
* Includes old + new custom fields
* Mandatory before migration

---

## 🧱 Additional Structures

### Workflows


ibc/workflows/


### Permissions


ibc/permissions/



### Shared Utilities


ibc/utils/


---

## 📝 Change Management

* Every change must:

  * Append to `Changelog.md`
  * Include date, file, reason
  * Mention performance impact if any

---

## 🧠 Agent Mindset

* Performance first
* Fixtures before code
* Ask before creating doctypes
* Never touch core
* Always migration-safe

---

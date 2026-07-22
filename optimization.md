# IBC App Performance Optimization Guide

This document contains performance issues identified in the IBC app and recommended optimizations.

---

## Table of Contents

1. [Critical Issues](#critical-issues)
2. [Scheduler Events Optimization](#scheduler-events-optimization)
3. [DocType Triggers Optimization](#doctype-triggers-optimization)
4. [Hooks.py Optimization](#hookspy-optimization)
5. [Custom Reports Optimization](#custom-reports-optimization)
6. [General Code Quality Issues](#general-code-quality-issues)
7. [Implementation Priority](#implementation-priority)

---

## Critical Issues

### 1. Scheduler `all.py` Runs Every Minute - HIGH IMPACT

**File:** `ibc/scheduler_events/all.py`

**Problem:** The `all()` function runs every minute and executes:
1. `repost_entries()` - Heavy stock reposting operation
2. A full table UPDATE on `tabItem` with a correlated subquery

```python
# CURRENT CODE - RUNS EVERY MINUTE
def all():
    repost_entries()
    frappe.db.sql("""
    update tabItem set tabItem.summary_stock = (select sum(tabBin.actual_qty) from tabBin join tabWarehouse on tabBin.warehouse = tabWarehouse.name where tabWarehouse.summery_stock = 1 and tabBin.item_code = tabItem.name) 
    """)
```

**Impact:** 
- Extremely high database load
- Locks on `tabItem` table affecting all item operations
- `repost_entries()` is resource-intensive

**Recommendation:**
```python
# OPTIMIZED - Move to hourly or add conditions
@frappe.whitelist()
def all():
    # Only repost if there are pending entries
    pending = frappe.db.count("Repost Item Valuation", {"status": "Queued"})
    if pending:
        repost_entries()
    
    # Only update items that actually changed (use a flag or timestamp)
    # Or move this to hourly scheduler
```

**Action Required:** 
- [ ] Move `summary_stock` update to hourly scheduler
- [ ] Add condition to only run `repost_entries()` when needed
- [ ] Consider adding index on `tabWarehouse.summery_stock`

---

### 2. Daily Scheduler - Redundant Queries

**File:** `ibc/scheduler_events/daily.py`

**Problem:** 14 separate UPDATE statements that could be combined:

```python
# CURRENT CODE - 14 SEPARATE QUERIES
frappe.db.sql("""update `tabDelivery Note Item` join `tabItem` ... set brand = ...""")
frappe.db.sql("""update `tabDelivery Note Item` join `tabItem` ... set item_group = ...""")
# ... repeated for each DocType
```

**Impact:**
- 14 full table scans instead of 7
- Each query locks tables separately

**Recommendation:**
```python
# OPTIMIZED - Combine brand and item_group updates
def daily():
    tables = [
        "Delivery Note Item",
        "Purchase Invoice Item", 
        "Purchase Order Item",
        "Purchase Receipt Item",
        "Sales Invoice Item",
        "Sales Order Item"
    ]
    
    for table in tables:
        frappe.db.sql("""
            UPDATE `tab{table}` t
            JOIN `tabItem` i ON t.item_code = i.name
            SET t.brand = i.brand, t.item_group = i.item_group
            WHERE t.brand != i.brand OR t.item_group != i.item_group
        """.format(table=table))
    
    # Stock Ledger Entry - only update where NULL
    frappe.db.sql("""
        UPDATE `tabStock Ledger Entry` sle
        JOIN `tabItem` i ON sle.item_code = i.name
        SET sle.brand = i.brand, sle.item_group = i.item_group
        WHERE sle.brand IS NULL OR sle.item_group IS NULL
    """)
    
    frappe.db.commit()
```

**Action Required:**
- [ ] Combine UPDATE statements (14 → 7 queries)
- [ ] Add WHERE clause to only update changed records
- [ ] Add `frappe.db.commit()` at the end

---

### 3. Hourly Scheduler - Inefficient Queries

**File:** `ibc/scheduler_events/hourly.py`

**Problem:** 
1. Unused imports (`json`, `ast`, `requests`, `OAuth1`)
2. Query on line 16 has wrong join condition

```python
# BUG: Wrong join condition
frappe.db.sql("""update tabBin join tabItem on tabBin.item_code = tabItem.name ...""")
# Should be: tabItem.item_code = tabBin.item_code OR tabItem.name = tabBin.item_code
```

**Recommendation:**
```python
# OPTIMIZED
from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def hourly():
    # Update valuation_rate only where different
    frappe.db.sql("""
        UPDATE tabItem i
        INNER JOIN tabBin b ON i.name = b.item_code
        INNER JOIN tabWarehouse w ON w.name = b.warehouse
        SET i.valuation_rate = b.valuation_rate
        WHERE w.is_main_warehouse = 1 
        AND i.valuation_rate != b.valuation_rate
    """)
    
    # Sync brand to Bin - only where different
    frappe.db.sql("""
        UPDATE tabBin b
        INNER JOIN tabItem i ON i.name = b.item_code
        SET b.brand = i.brand
        WHERE b.brand != i.brand OR b.brand IS NULL
    """)
    
    # Update Quotation creator
    frappe.db.sql("""
        UPDATE tabQuotation 
        SET creator = owner 
        WHERE creator IS NULL
    """)
    
    # Sync item_group to Bin - FIX: correct join
    frappe.db.sql("""
        UPDATE tabBin b
        INNER JOIN tabItem i ON i.name = b.item_code
        SET b.item_group = i.item_group
        WHERE b.item_group != i.item_group OR b.item_group IS NULL
    """)
    
    frappe.db.commit()
```

**Action Required:**
- [ ] Remove unused imports
- [ ] Fix join condition bug
- [ ] Add WHERE clauses to limit updates
- [ ] Add `frappe.db.commit()`

---

## DocType Triggers Optimization

### 4. Empty Trigger Functions - MAJOR OVERHEAD

**Problem:** Most trigger files contain 11 empty `pass` functions registered in hooks.py. Each function call has overhead even if it does nothing.

**Files Affected:** 30+ trigger files including:
- `sales_invoice.py` - All 11 functions are empty `pass`
- `quotation.py` - All 11 functions are empty `pass`
- `delivery_note.py` - All 11 functions are empty `pass`
- `purchase_invoice.py` - All 11 functions are empty `pass`
- `employee.py` - All 7 functions are empty `pass`
- Many more...

**Current Pattern:**
```python
# CURRENT - 11 empty functions per file
@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
# ... 9 more empty functions
```

**Impact:**
- ~46 DocTypes × ~11 events = ~506 function calls registered
- Most are empty `pass` statements
- Each call has import and function call overhead
- Slows down every document operation

**Recommendation:**

**Option A (Recommended):** Remove empty functions from hooks.py
```python
# hooks.py - Only register functions that have actual code
doc_events = {
    "Journal Entry": {
        "validate": "ibc.doctype_triggers.accounting.journal_entry.journal_entry.validate",
    },
    "Payment Entry": {
        "validate": "ibc.doctype_triggers.accounting.payment_entry.payment_entry.validate",
        "on_submit": "ibc.doctype_triggers.accounting.payment_entry.payment_entry.on_submit",
        "before_save": "ibc.doctype_triggers.accounting.payment_entry.payment_entry.before_save",
    },
    # ... only non-empty functions
}
```

**Option B:** Keep structure but remove from hooks.py until needed

**Action Required:**
- [ ] Audit all trigger files to identify which have actual code
- [ ] Remove empty function registrations from hooks.py
- [ ] Keep trigger files for future use but don't register empty functions

---

### 5. Unnecessary `@frappe.whitelist()` on Trigger Functions

**Problem:** All trigger functions have `@frappe.whitelist()` decorator, but these are internal hooks, not API endpoints.

```python
# CURRENT - Unnecessary decorator
@frappe.whitelist()
def validate(doc, method=None):
    pass
```

**Impact:**
- Exposes internal functions as API endpoints (security risk)
- Adds decorator overhead

**Recommendation:**
```python
# OPTIMIZED - Remove decorator from non-API functions
def validate(doc, method=None):
    # Only add @frappe.whitelist() for functions that need API access
    pass
```

**Action Required:**
- [ ] Remove `@frappe.whitelist()` from all trigger functions
- [ ] Keep decorator only on actual API endpoints like `bulk_publish_website_items`

---

### 6. SQL Injection Vulnerability in customer.py

**File:** `ibc/doctype_triggers/selling/customer/customer.py`

**Problem:** String formatting in SQL query (SQL injection risk)

```python
# VULNERABLE CODE
attachments = frappe.db.sql(
    """ Select file_name, file_url
        from `tabFile` where `tabFile`.attached_to_doctype = "Lead"
        and `tabFile`.attached_to_name = "{name}"
    """.format(name=doc.lead_name), as_dict=1)
```

**Recommendation:**
```python
# SECURE CODE - Use parameterized query
attachments = frappe.db.sql("""
    SELECT file_name, file_url
    FROM `tabFile` 
    WHERE attached_to_doctype = 'Lead'
    AND attached_to_name = %s
""", (doc.lead_name,), as_dict=1)
```

**Action Required:**
- [ ] Fix SQL injection vulnerability
- [ ] Audit all files for similar issues

---

### 7. Unnecessary `frappe.msgprint` in Production Code

**File:** `ibc/doctype_triggers/selling/customer/customer.py`

```python
# DEBUG CODE LEFT IN PRODUCTION
existing_lead = frappe.db.exists("Lead", {"mobile_no": doc.mobile_no})
frappe.msgprint(existing_lead)  # <-- Remove this
```

**Action Required:**
- [ ] Remove debug `frappe.msgprint` statements

---

## Custom Reports Optimization

### 8. `new_gross_profit.py` - Heavy Queries

**File:** `ibc/ibc/report/new_gross_profit/new_gross_profit.py`

**Problems:**
1. `load_stock_ledger_entries()` loads ALL stock ledger entries for the company
2. Correlated subqueries in main SELECT (lines 347-352)
3. `load_product_bundle()` loads ALL packed items

```python
# CURRENT - Loads entire SLE table
def load_stock_ledger_entries(self):
    res = frappe.db.sql("""select item_code, voucher_type, voucher_no,
            voucher_detail_no, stock_value, warehouse, actual_qty as qty
        from `tabStock Ledger Entry`
        where company=%(company)s and is_cancelled = 0
        order by item_code desc, warehouse desc, posting_date desc,
            posting_time desc, creation desc""", self.filters, as_dict=True)
```

**Impact:** For companies with millions of SLE records, this loads everything into memory.

**Recommendation:**
```python
# OPTIMIZED - Only load SLE for items in the invoice list
def load_stock_ledger_entries(self):
    if not self.si_list:
        self.sle = {}
        return
    
    item_codes = list(set([d.item_code for d in self.si_list]))
    warehouses = list(set([d.warehouse for d in self.si_list if d.warehouse]))
    
    res = frappe.db.sql("""
        SELECT item_code, voucher_type, voucher_no,
            voucher_detail_no, stock_value, warehouse, actual_qty as qty
        FROM `tabStock Ledger Entry`
        WHERE company = %(company)s 
        AND is_cancelled = 0
        AND item_code IN %(item_codes)s
        AND warehouse IN %(warehouses)s
        ORDER BY item_code desc, warehouse desc, posting_date desc,
            posting_time desc, creation desc
    """, {"company": self.filters.company, "item_codes": item_codes, "warehouses": warehouses}, as_dict=True)
    # ... rest of code
```

**Action Required:**
- [ ] Filter SLE by items in invoice list
- [ ] Consider pagination for large date ranges
- [ ] Move correlated subqueries to JOINs

---

### 9. `stock_balances.py` - Missing Index Usage

**File:** `ibc/ibc/report/stock_balances/stock_balances.py`

**Problem:** Uses `force index (posting_sort_index)` which may not be optimal

```python
from `tabStock Ledger Entry` sle force index (posting_sort_index)
```

**Recommendation:** Let MySQL optimizer choose the index, or verify the index exists and is appropriate.

**Action Required:**
- [ ] Verify `posting_sort_index` exists
- [ ] Test query performance with and without force index

---

### 10. `customized_sales_analytics.py` - Repeated Queries

**File:** `ibc/ibc/report/customized_sales_analytics/customized_sales_analytics.py`

**Problem:** Multiple similar queries with slight variations, code duplication

**Action Required:**
- [ ] Refactor to reduce code duplication
- [ ] Use parameterized base query

---

## Hooks.py Optimization

### 11. Excessive doc_events Registration

**File:** `ibc/hooks.py`

**Problem:** 46 DocTypes with ~11 events each = ~506 event registrations, most pointing to empty functions.

**Current Size:** ~53KB (very large for a hooks file)

**Recommendation:** Only register events that have actual implementations.

**Action Required:**
- [ ] Create a script to audit which trigger functions have actual code
- [ ] Remove empty registrations from hooks.py
- [ ] Expected reduction: ~80% of registrations

---

## General Code Quality Issues

### 12. Unused Imports

**Files with unused imports:**
- `daily.py`: `json`, `ast`, `requests`, `OAuth1`
- `hourly.py`: `json`, `ast`, `requests`, `OAuth1`
- `item.py`: `json`, `ast`, `requests`

**Action Required:**
- [ ] Remove unused imports from all files

---

### 13. Missing `frappe.db.commit()` After Bulk Updates

**Files:** `all.py`, `daily.py`, `hourly.py`

**Problem:** Bulk SQL updates without explicit commit may cause issues.

**Action Required:**
- [ ] Add `frappe.db.commit()` after bulk operations

---

### 14. Typo in Database Field

**File:** `all.py`

```python
# TYPO: "summery_stock" should be "summary_stock"
where tabWarehouse.summery_stock = 1
```

**Action Required:**
- [ ] Verify correct field name in Warehouse DocType
- [ ] Fix typo if needed

---

## Implementation Priority

### Phase 1 - Critical (Do First)
| # | Issue | File | Impact |
|---|-------|------|--------|
| 1 | Move `all.py` to hourly | `scheduler_events/all.py` | HIGH - Reduces DB load by 60x |
| 2 | Combine daily.py queries | `scheduler_events/daily.py` | HIGH - 50% fewer queries |
| 3 | Fix SQL injection | `customer/customer.py` | CRITICAL - Security |
| 4 | Remove empty hooks | `hooks.py` | HIGH - Faster doc operations |

### Phase 2 - Important
| # | Issue | File | Impact |
|---|-------|------|--------|
| 5 | Remove `@frappe.whitelist()` from triggers | All trigger files | MEDIUM - Security + Performance |
| 6 | Fix hourly.py join bug | `scheduler_events/hourly.py` | MEDIUM - Data integrity |
| 7 | Optimize gross_profit report | `new_gross_profit.py` | MEDIUM - Report speed |

### Phase 3 - Cleanup
| # | Issue | File | Impact |
|---|-------|------|--------|
| 8 | Remove unused imports | Multiple files | LOW - Code cleanliness |
| 9 | Remove debug msgprint | `customer.py` | LOW - User experience |
| 10 | Add db.commit() | Scheduler files | LOW - Data consistency |

---

## Quick Wins Summary

1. **Move `all.py` logic to hourly** - Immediate 60x reduction in scheduler load
2. **Remove empty trigger registrations** - Faster document operations
3. **Fix SQL injection** - Critical security fix
4. **Combine daily.py queries** - 50% fewer database queries

---

## Estimated Performance Improvement

| Area | Current | After Optimization | Improvement |
|------|---------|-------------------|-------------|
| Scheduler load | Every minute | Hourly | 60x reduction |
| Daily sync queries | 14 queries | 7 queries | 50% reduction |
| Doc event overhead | ~506 registrations | ~50 registrations | 90% reduction |
| Report load time | Full table scan | Filtered query | 10-100x faster |

---

## Next Steps

1. Review this document
2. Prioritize which optimizations to implement
3. Test changes on development environment
4. Deploy to production with monitoring

---

*Generated: 2025-02-15*
*App: IBC v0.0.1*

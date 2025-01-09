// Copyright (c) 2025, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Person Target"] = {
	"filters": [
    {
        fieldname: "posting_date_from",
        label: __("From Date"),
        fieldtype: "Date",
        default: "2024-01-01",  // Set default to January 1, 2024
        reqd: 1,
    },
    {
        fieldname: "to_posting_date",
        label: __("To Date"),
        fieldtype: "Date",
        default: "2024-12-31",  // Set default to December 31, 2024
        reqd: 1,
    },
    {
        fieldname: "sales_person",
        label: __("Sales Person"),
        fieldtype: "Link",
        options: "Sales Person",
    },
    {
        fieldname: "is_return",
        label: __("Is Return"),
        fieldtype: "Check",
        default: 0,  
    }
]
};

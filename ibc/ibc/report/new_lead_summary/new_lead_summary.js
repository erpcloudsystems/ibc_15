// Copyright (c) 2026, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["New Lead Summary"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": __("From Date"),
			"width": 150,
			"default": frappe.datetime.month_start(),
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": __("To Date"),
			"width": 150,
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
	]
};

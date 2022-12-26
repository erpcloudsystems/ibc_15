// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Discounted Sales invoice Filtered (Sales Director)"] = {
	"filters": [
	{
		"fieldname": "from_date",
		"label": __("From Date"),
		"fieldtype": "Date",
		"default": frappe.defaults.get_user_default("year_start_date")
	},
	{
		"fieldname": "to_date",
		"label": __("To Date"),
		"fieldtype": "Date",
		"default": frappe.defaults.get_user_default("year_end_date")
	},
	{
		"fieldname":"brand",
		"label": __("Brand"),
		"fieldtype": "Link",
		"options": "Brand"
	}
]
};

// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Spare Parts Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			default: frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"installation_engineer",
			"label": __("installation_engineer"),
			"fieldtype": "Link",
			"options" : "User",
			"reqd": 0
		}
	]
}


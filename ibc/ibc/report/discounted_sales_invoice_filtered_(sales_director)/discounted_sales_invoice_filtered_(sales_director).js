// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Discounted Sales invoice Filtered (Sales Director)"] = {
	"filters": [
	{
		"fieldname": "from_date",
		"label": __("From Date"),
		"fieldtype": "Date",
		"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
	},
	{
		"fieldname": "to_date",
		"label": __("To Date"),
		"fieldtype": "Date",
		"default": frappe.datetime.get_today()
	},
	{
		"fieldname":"brand",
		"label": __("Brand"),
		"fieldtype": "Link",
		"options": "Brand"
	},
	{
		"fieldname":"sales_person",
		"label": __("Sales Person"),
		"fieldtype": "Link",
		"options": "Sales Person",
		'width': 150,
		"get_query": function() {
			return {
				"filters": {
					"parent_sales_person": ["in", ['Sales Director','6th October','Alexandria','Head Office','Demo','Hurgada','Down Town']],
				}
			}
		}
	},
	{
			"fieldname": "show_only_maintain_stock",
			"label": __("Show Only Maintain Stock"),
			"fieldtype": "Check",
			"default": true
	},
]
};

// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Discounted Sales invoice Filtered (Sales Director)"] = {
	"filters": [
		{
			'fieldname':'from_date',
			'fieldtype':'Date',
			'label':__('From Date'),
			'width':150,
			default: frappe.datetime.add_months(frappe.datetime.get_today(),-1),

		},
		{
			'fieldname':'to_date',
			'fieldtype':'Date',
			'label':__('To Date'),
			'width':150,
			default: frappe.datetime.get_today(),
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
						"parent_sales_person": ["in", ['6th October','Alexandria','Down Town','Head Office','Hurgada','New Cairo']],
					}
				}
			}

		},

	]
};

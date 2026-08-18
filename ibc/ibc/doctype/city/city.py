# Copyright (c) 2026, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class City(Document):
	def onload(self):
		zones = frappe.get_all("Zone", filters={"city": self.name}, pluck="name")
		self.set("zone", [{"zone": zone} for zone in zones])

	def on_update(self):
		linked_zones = {row.zone for row in self.zone}
		existing_zones = set(frappe.get_all("Zone", filters={"city": self.name}, pluck="name"))

		for zone in linked_zones - existing_zones:
			frappe.db.set_value("Zone", zone, "city", self.name)

		for zone in existing_zones - linked_zones:
			frappe.db.set_value("Zone", zone, "city", None)

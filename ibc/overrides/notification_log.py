import re

import frappe

# The dropdown wraps each notification in its own <a> (the whole row navigates
# to the document), so any <a> tag already present inside the stored
# description/title is a nested anchor - invalid HTML that browsers silently
# mangle, producing empty/duplicated fragments in the notification dropdown.
# Strip anchor tags here (keeping their text) since the row is already a link.
_ANCHOR_TAG_RE = re.compile(r"</?a\b[^>]*>", re.IGNORECASE)


def _strip_anchor_tags(html):
	if not html:
		return html
	return _ANCHOR_TAG_RE.sub("", html)


@frappe.whitelist()
def get_notification_logs(limit=20):
	notification_logs = frappe.db.get_list(
		"Notification Log", fields=["*"], limit=limit, order_by="modified desc"
	)

	for log in notification_logs:
		log.description = _strip_anchor_tags(log.description)
		log.title = _strip_anchor_tags(log.title)

	users = [log.from_user for log in notification_logs]
	users = [*set(users)]  # remove duplicates
	user_info = frappe._dict()

	for user in users:
		frappe.utils.add_user_info(user, user_info)

	return {"notification_logs": notification_logs, "user_info": user_info}

from __future__ import unicode_literals
import frappe


def dedupe_notification_logs():
    """Delete duplicate Notification Log rows created by misbehaving triggers
    (e.g. a Notification rule or event firing more than once for the same
    document), keeping only the earliest row per
    (for_user, document_type, document_name, subject).
    """
    duplicate_groups = frappe.db.sql(
        """
        SELECT for_user, document_type, document_name, subject, COUNT(*) AS cnt
        FROM `tabNotification Log`
        WHERE document_name IS NOT NULL AND document_name != ''
            AND creation > NOW() - INTERVAL 2 DAY
        GROUP BY for_user, document_type, document_name, subject
        HAVING cnt > 1
        """,
        as_dict=True,
    )

    for group in duplicate_groups:
        rows = frappe.get_all(
            "Notification Log",
            filters={
                "for_user": group.for_user,
                "document_type": group.document_type,
                "document_name": group.document_name,
                "subject": group.subject,
            },
            fields=["name"],
            order_by="creation asc",
        )
        extra_names = [r.name for r in rows[1:]]
        if extra_names:
            frappe.db.delete("Notification Log", {"name": ["in", extra_names]})

    if duplicate_groups:
        frappe.db.commit()

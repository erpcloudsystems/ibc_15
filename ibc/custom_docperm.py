# ecs_newtech/custom_docperm.py
import frappe
import json
import os
import glob

SNAPSHOT_FOLDER = "permission_snapshots"
SNAPSHOT_FILE = "custom_docperm.json"

#
def snapshot_custom_docperm():
    """
    Daily scheduler task: Export all Custom DocPerm to a single JSON file.
    Deletes any existing snapshot files first (keeps only one file).
    """
    folder_path = frappe.get_site_path(SNAPSHOT_FOLDER)
    os.makedirs(folder_path, exist_ok=True)
    
    # Delete all existing snapshot files (keep only one)
    existing_files = glob.glob(os.path.join(folder_path, "custom_docperm*.json"))
    for old_file in existing_files:
        try:
            os.remove(old_file)
            frappe.logger().info(f"Deleted old snapshot: {old_file}")
        except Exception as e:
            frappe.logger().error(f"Failed to delete {old_file}: {e}")
    
    # Fetch all custom permissions
    perms = frappe.get_all("Custom DocPerm", fields=["*"])
    
    # Save snapshot to single file
    filename = os.path.join(folder_path, SNAPSHOT_FILE)
    with open(filename, "w") as f:
        json.dump(perms, f, indent=2, default=str)
    
    frappe.logger().info(f"Custom DocPerm snapshot saved: {filename} ({len(perms)} records)")


def restore_permissions():
    """
    After migrate hook: Delete all existing Custom DocPerm records,
    then re-import from the exported snapshot file.
    """
    snapshot_path = frappe.get_site_path(SNAPSHOT_FOLDER, SNAPSHOT_FILE)
    
    if not os.path.exists(snapshot_path):
        frappe.logger().warning(f"No snapshot file found at {snapshot_path}, skipping restore")
        return
    
    # Load permissions from snapshot
    with open(snapshot_path, "r") as f:
        perms = json.load(f)
    
    if not perms:
        frappe.logger().info("No permissions in snapshot file, skipping restore")
        return
    
    # Delete all existing Custom DocPerm records
    existing_perms = frappe.get_all("Custom DocPerm", pluck="name")
    for perm_name in existing_perms:
        try:
            frappe.delete_doc("Custom DocPerm", perm_name, ignore_permissions=True, force=True)
        except Exception as e:
            frappe.logger().error(f"Failed to delete Custom DocPerm {perm_name}: {e}")
    
    frappe.logger().info(f"Deleted {len(existing_perms)} existing Custom DocPerm records")
    
    # Insert permissions from snapshot
    inserted_count = 0
    for perm in perms:
        # Remove fields that shouldn't be inserted
        perm.pop("name", None)
        perm.pop("creation", None)
        perm.pop("modified", None)
        perm.pop("modified_by", None)
        perm.pop("owner", None)
        perm.pop("docstatus", None)
        perm.pop("idx", None)
        
        try:
            doc = frappe.get_doc({
                "doctype": "Custom DocPerm",
                **perm
            })
            doc.insert(ignore_permissions=True)
            inserted_count += 1
        except Exception as e:
            frappe.logger().error(f"Failed to insert Custom DocPerm: {e}")
    
    frappe.db.commit()
    frappe.logger().info(f"Restored {inserted_count} Custom DocPerm records from snapshot")
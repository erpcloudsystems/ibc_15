// frappe.ui.form.on('Item Price', {

// 	refresh(frm) {
// 	    frm.add_custom_button(__("Update Website Item"), function() {
//             frappe.call({
//                 method: 'frappe.client.get_value',
//                 args: {
//                     'doctype': 'Sales Order',
//                     'filters': {'name': frm.doc.sales_order},
//                     'fieldname': [
//                         'customer',
//                     ]
//                 },
//                 callback: function(r) {
//                     if (r.message) {
//                    frm.silently_set_value('customer', r.message.customer)
            
              
//                     }
              
//                 }
//             });       
//     });

// 	}
// });

// frappe.ui.form.on('Item', {
//     refresh: function(frm) {
//         // Call the validation_rate_fetch function when the document is refreshed
//         frappe.call({
//             method: 'ibc.doctype_triggers.stock.item.item.validation_rate_fetch',
//             args: {
//                 'doc': frm.doc
//             },
//             callback: function(response) {
//                 // Optionally, handle the response here if needed
//                 frm.refresh_field('valuation_rate');  // Refresh the field to show the updated value
//             }
//         });
//     }
// });

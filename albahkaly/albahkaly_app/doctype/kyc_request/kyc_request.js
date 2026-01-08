// Copyright (c) 2026, Sowaan Pvt. Ltd and contributors
// For license information, please see license.txt

// frappe.ui.form.on("KYC Request", {
// 	refresh(frm) {
frappe.ui.form.on("KYC Request", {
    refresh(frm) {
        // ❌ Do not show button if:
        // 1. Document is new (not saved)
        // 2. Customer already created
        if (frm.is_new() || frm.doc.created_customer) {
            return;
        }
        
        // show only if customer not created yet
        if (!frm.doc.created_customer) {
            frm.add_custom_button(
                __("Create Customer"),
                () => {
                    frappe.call({
                        method: "albahkaly.albahkaly_app.doctype.kyc_request.kyc_request.create_customer_from_kyc",
                        args: {
                            kyc_name: frm.doc.name
                        },
                        freeze: true,
                        freeze_message: __("Creating Customer...")
                    }).then(r => {
                        if (r.message) {
                            frappe.msgprint(
                                __("Customer Created: {0}", [r.message])
                            );
                            frm.reload_doc();
                        }
                    });
                }
            );
        }
    }
});

// 	},
// });

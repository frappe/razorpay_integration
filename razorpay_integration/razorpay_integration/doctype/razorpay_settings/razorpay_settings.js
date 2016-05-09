// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Razorpay Settings', {
	refresh: function(frm) {
		frm.add_custom_button(__("Razorpay Logs"), function() {
			frappe.set_route("List", "Razorpay Log");
		})
		frm.add_custom_button(__("Payment Logs"), function() {
			frappe.set_route("List", "Razorpay Payment");
		});
		frm.add_custom_button(__("Payment Gateway Accounts"), function() {
			frappe.route_options = {"payment_gateway": "Razorpay"};
			frappe.set_route("List", "Payment Gateway Account");
		});
	}
});

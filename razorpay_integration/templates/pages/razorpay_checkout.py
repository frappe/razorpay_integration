# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from razorpay_integration.exceptions import InvalidRequest, AuthenticationError, GatewayError

no_cache = 1
no_sitemap = 1

def get_context(context):
	context.no_cache = 1
	payment_req = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.docname)
	
	if payment_req.status == "Paid":
		frappe.redirect_to_message(_('Already Paid'), _('You have already paid for this order'))
		return
	
	reference_doc = frappe.get_doc(payment_req.reference_doctype, payment_req.reference_name)
	context.customer_name =	reference_doc.customer_name
	context.api_key = frappe.db.get_value("Razorpay Settings", None, "api_key")
	context.company = reference_doc.company
	context.doc = payment_req
	context.user = frappe.session.user
	
@frappe.whitelist(allow_guest=True)
def make_payment(razorpay_payment_id, options, reference_doctype, reference_docname):
	try:
		razorpay_express_payment = frappe.get_doc({
			"doctype": "Razorpay Express Payment",
			"razorpay_payment_id": razorpay_payment_id,
			"data": options,
			"reference_doctype": reference_doctype,
			"reference_docname": reference_docname
		})
	
		razorpay_express_payment.insert(ignore_permissions=True)
	
		if frappe.db.get_value("Razorpay Express Payment", razorpay_express_payment.name, "status") == "Authorized":
			return {
				"redirect_to": razorpay_express_payment.flags.redirect_to or "razorpay-payment-success",
				"status": 200
			}
			
	except AuthenticationError, e:
		frappe.redirect_to_message(_('Already Paid'), _('You have already paid for this order'))
		return 
	except InvalidRequest, e:
		return {
			"redirect_to": "razorpay-payment-error",
			"status": 200
		}
	except GatewayError, e:
		return {
			"redirect_to": "razorpay-payment-error",
			"status": 200
		}


	
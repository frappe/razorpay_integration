# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _
from frappe.utils import get_url
from razorpay_integration.utils import make_log_entry
from razorpay_integration.razorpay_requests import get_request, post_request
from razorpay_integration.exceptions import InvalidRequest, AuthenticationError, GatewayError

class RazorpayPayment(Document):
	def on_update(self):
		api_key, api_secret = frappe.db.get_value("Razorpay Settings", None, ["api_key", "api_secret"])
		if self.status != "Authorized":
			confirm_payment(self, api_key, api_secret)
		set_redirect(self)

def authorise_payment():
	api_key, api_secret = frappe.db.get_value("Razorpay Settings", None, ["api_key", "api_secret"])
	for doc in frappe.get_all("Razorpay Express Payment", filters={"status": "Created"},
		fields=["name", "data", "reference_doctype", "reference_docname"]):
		
		confirm_payment(doc, api_key, api_secret)
		set_redirect(doc)

def confirm_payment(doc, api_key, api_secret):
	"""
		An authorization is performed when user’s payment details are successfully authenticated by the bank.
		The money is deducted from the customer’s account, but will not be transferred to the merchant’s account
		until it is explicitly captured by merchant.
	"""
	resp = get_request("https://api.razorpay.com/v1/payments/{0}".format(doc.name), 
		auth=frappe._dict({"api_key": api_key, "api_secret": api_secret}))
	
	if resp.get("status") == "authorized":
		frappe.db.set_value("Razorpay Payment", doc.name, "status", "Authorized")
		doc.flags.status_changed_to = "Authorized"
		
def capture_payment():
	"""
		Verifies the purchase as complete by the merchant.
		After capture, the amount is transferred to the merchant within T+3 days
		where T is the day on which payment is captured.
		
		Note: Attempting to capture a payment whose status is not authorized will produce an error.
	"""
	
	api_key, api_secret = frappe.db.get_value("Razorpay Settings", None, ["api_key", "api_secret"])
	
	for doc in frappe.get_all("Razorpay Payment", filters={"status": "Authorized"},
		fields=["name", "data"]):
		
		try:
			resp = post_request("https://api.razorpay.com/v1/payments/{0}/capture".format(doc.name),
				data={"amount": json.loads(doc.data).get("amount")},
				auth=frappe._dict({"api_key": api_key, "api_secret": api_secret}))
			if resp.get("status") == "captured":
				frappe.db.set_value("Razorpay Payment", doc.name, "status", "Captured")
			
		except AuthenticationError, e:
			make_log_entry(e.message, json.dumps({"api_key": api_key, "api_secret": api_secret,
				"doc_name": doc.name, "status": doc.status}))
			
		except InvalidRequest, e:
			make_log_entry(e.message, json.dumps({"api_key": api_key, "api_secret": api_secret,
				"doc_name": doc.name, "status": doc.status}))
			
		except GatewayError, e:
			make_log_entry(e.message, json.dumps({"api_key": api_key, "api_secret": api_secret,
				"doc_name": doc.name, "status": doc.status}))

def capture_missing_payments():
	api_key, api_secret = frappe.db.get_value("Razorpay Settings", None, ["api_key", "api_secret"])
	
	resp = get_request("https://api.razorpay.com/v1/payments",
		auth=frappe._dict({"api_key": api_key, "api_secret": api_secret}))
	
	for payment in resp.get("items"):
		if payment.get("status") == "authorized" and not frappe.db.exists("Razorpay Payment", payment.get("id")):
			razorpay_payment = frappe.get_doc({
				"doctype": "Razorpay Payment",
				"razorpay_payment_id": payment.get("id"),
				"data": {
					"amount": payment["amount"],
					"description": payment["description"],
					"email": payment["email"],
					"contact": payment["contact"],
					"payment_request": payment["notes"]["payment_request"],
					"reference_doctype": payment["notes"]["reference_doctype"],
					"reference_docname": payment["notes"]["reference_docname"]
				},
				"status": "Authorized",
				"reference_doctype": "Payment Request",
				"reference_docname": payment["notes"]["payment_request"]
			})
	
			razorpay_payment.insert(ignore_permissions=True)

def set_redirect(razorpay_express_payment):
	"""
		ERPNext related redirects.
		You need to set Razorpay Payment.flags.redirect_to on status change.
		Called via RazorpayPayment.on_update
	"""
	if "erpnext" not in frappe.get_installed_apps():
		return

	if not razorpay_express_payment.flags.status_changed_to:
		return
		
	reference_doctype = razorpay_express_payment.reference_doctype
	reference_docname = razorpay_express_payment.reference_docname
		
	if not (reference_doctype and reference_docname):
		return

	reference_doc = frappe.get_doc(reference_doctype,  reference_docname)
	shopping_cart_settings = frappe.get_doc("Shopping Cart Settings")
	
	if razorpay_express_payment.flags.status_changed_to == "Authorized":
		reference_doc.run_method("set_as_paid")

		# if shopping cart enabled and in session
		if (shopping_cart_settings.enabled
			and hasattr(frappe.local, "session")
			and frappe.local.session.user != "Guest"):

			success_url = shopping_cart_settings.payment_success_url
			if success_url:
				razorpay_express_payment.flags.redirect_to = ({
					"Orders": "orders",
					"Invoices": "invoices",
					"My Account": "me"
				}).get(success_url, "me")
			else:
				razorpay_express_payment.flags.redirect_to = get_url("/orders/{0}".format(reference_doc.reference_name))


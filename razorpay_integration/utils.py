# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def get_payment_url(doc, method):
	if doc.docstatus == 1:
		if doc.payment_gateway == "Razorpay":
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = "./razorpay_checkout?payment_request={0}".format(doc.name)
	else:
		frappe.respond_as_web_page(_("Invalid Payment Request"),
			_("Payment Request has been canceled by vendor"), success=False,
			http_status_code=frappe.ValidationError.http_status_code)

def validate_price_list_currency(doc, method):
	'''Called from Shopping Cart Settings hook'''
	if doc.enabled and doc.enable_checkout:
		if not doc.payment_gateway_account:
			doc.enable_checkout = 0
			return

		payment_gateway_account = frappe.get_doc("Payment Gateway Account", doc.payment_gateway_account)

		if payment_gateway_account.payment_gateway=="Razorpay":
			price_list_currency = frappe.db.get_value("Price List", doc.price_list, "currency")

			validate_transaction_currency(price_list_currency)

			if price_list_currency != payment_gateway_account.currency:
				frappe.throw(_("Currency '{0}' of Price List '{1}' should be same as the Currency '{2}' of Payment Gateway Account '{3}'").format(price_list_currency, doc.price_list, payment_gateway_account.currency, payment_gateway_account.name))

def validate_transaction_currency(transaction_currency):
	if transaction_currency != "INR":
		frappe.throw(_("Please select another payment method. Razorpay does not support transactions in currency '{0}'").format(transaction_currency))

def make_log_entry(error, params):
	frappe.db.rollback()

	frappe.get_doc({
		"doctype": "Razorpay Log",
		"error": error,
		"params": params
	}).insert(ignore_permissions=True)

	frappe.db.commit()

def get_razorpay_settings():
	settings = frappe.db.get_singles_dict('Razorpay Settings')

	if not settings.api_key and frappe.local.conf.get('Razorpay Settings', {}).get('api_key'):
		settings = frappe._dict(frappe.local.conf['Razorpay Settings'])

	return settings

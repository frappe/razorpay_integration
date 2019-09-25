# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from razorpay_integration.utils import get_razorpay_settings
from razorpay_integration.razorpay_requests import get_request
from razorpay_integration.exceptions import AuthenticationError

class RazorpaySettings(Document):
	def validate(self):
		validate_razorpay_credentials(razorpay_settings=frappe._dict({
			"api_key": self.api_key,
			"api_secret": self.get_password(fieldname="api_secret")
		}))

	def on_update(self):
		create_payment_gateway_and_account()

def validate_razorpay_credentials(doc=None, method=None, razorpay_settings=None):
	if not razorpay_settings:
		razorpay_settings = get_razorpay_settings()

	try:
		get_request(url="https://api.razorpay.com/v1/payments", auth=frappe._dict({
			"api_key": razorpay_settings.api_key,
			"api_secret": razorpay_settings.api_secret
		}))
	except AuthenticationError as e:
		frappe.throw(_(e.message))

def create_payment_gateway_and_account():
	"""If ERPNext is installed, create Payment Gateway and Payment Gateway Account"""
	if "erpnext" not in frappe.get_installed_apps():
		return

	create_payment_gateway()
	create_payment_gateway_account()

def create_payment_gateway():
	# NOTE: we don't translate Payment Gateway name because it is an internal doctype
	if not frappe.db.exists("Payment Gateway", "Razorpay"):
		payment_gateway = frappe.get_doc({
			"doctype": "Payment Gateway",
			"gateway": "Razorpay"
		})
		payment_gateway.insert(ignore_permissions=True)

def create_payment_gateway_account():
	from erpnext.setup.setup_wizard.setup_wizard import create_bank_account

	company = frappe.db.get_value("Global Defaults", None, "default_company")
	if not company:
		return

	# NOTE: we translate Payment Gateway account name because that is going to be used by the end user
	bank_account = frappe.db.get_value("Account", {"account_name": _("Razorpay"), "company": company},
		["name", 'account_currency'], as_dict=1)

	if not bank_account:
		# check for untranslated one
		bank_account = frappe.db.get_value("Account", {"account_name": "Razorpay", "company": company},
			["name", 'account_currency'], as_dict=1)

	if not bank_account:
		# try creating one
		bank_account = create_bank_account({"company_name": company, "bank_account": _("Razorpay")})

	if not bank_account:
		frappe.throw(_("Payment Gateway Account not created, please create one manually."))

	# if payment gateway account exists, return
	if frappe.db.exists("Payment Gateway Account",
		{"payment_gateway": "Razorpay", "currency": bank_account.account_currency}):
		return

	try:
		frappe.get_doc({
			"doctype": "Payment Gateway Account",
			"is_default": 1,
			"payment_gateway": "Razorpay",
			"payment_account": bank_account.name,
			"currency": bank_account.account_currency
		}).insert(ignore_permissions=True)

	except frappe.DuplicateEntryError:
		# already exists, due to a reinstall?
		pass

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
			frappe.local.response["location"] = "./razorpay_checkout?doctype=Payment Request&docname={0}".format(doc.name)
	else:
		frappe.respond_as_web_page(_("Invalid Payment Request"),
			_("Payment Request has been canceled by vendor"), success=False,
			http_status_code=frappe.ValidationError.http_status_code)
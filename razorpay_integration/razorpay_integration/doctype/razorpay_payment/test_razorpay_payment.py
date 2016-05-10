# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
import json
from razorpay_integration.exceptions import InvalidRequest, AuthenticationError
from razorpay_integration.razorpay_integration.doctype.razorpay_payment.razorpay_payment import capture_payment

data = {
	"razorpay_settings": {
		"api_key": "rzp_test_lExD7NVL1JoKJJ",
		"api_secret": "ceM6bQs4vWgV30QcEu6yVil"
	},
	"options": {
		"key": "rzp_test_lExD7NVL1JoKJJ",
		"amount": 2000,
		"name": "_Test Company 1",
		"description": "Test Payment Request",
		"image": "./assets/erpnext/images/erp-icon.svg",
		"prefill": {
			"name": "_Test Customer 1",
			"email": "test@erpnext.com",
		},
		"theme": {
			"color": "#4B4C9D"
		}
	},
	"sanbox_response": {
		"entity": "payment",
		"amount": 500,
		"currency": "INR",
		"amount_refunded": 0,
		"refund_status": None,
		"email": "test@razorpay.com",
		"contact": "9364591752",
		"error_code": None,
		"error_description": None,
		"notes": {},
		"created_at": 1400826750
	}
}

class TestRazorpayPayment(unittest.TestCase):
	def test_razorpay_settings(self):
		razorpay_settings = frappe.get_doc("Razorpay Settings")
		razorpay_settings.update(data["razorpay_settings"])
		
		self.assertRaises(AuthenticationError, razorpay_settings.insert)
	
	def test_confirm_payment(self):
		razorpay_payment_id = "test_pay_{0}".format(frappe.generate_hash(length=14))
		razorpay_payment = make_payment(razorpay_payment_id=razorpay_payment_id,
			options=json.dumps(data["options"]))
			
		self.assertRaises(InvalidRequest, razorpay_payment.insert)
		
		razorpay_settings = frappe.get_doc("Razorpay Settings")
		razorpay_settings.update(data["razorpay_settings"])
		
		razorpay_payment_id = "test_pay_{0}".format(frappe.generate_hash(length=14))
		
		razorpay_payment = make_payment(razorpay_payment_id=razorpay_payment_id,
			options=json.dumps(data["options"]))
			
		razorpay_payment.flags.is_sandbox = True
		razorpay_payment.sanbox_response = data["sanbox_response"]
		razorpay_payment.sanbox_response.update({
			"id": razorpay_payment_id,
			"status": "authorized"
		})
		
		razorpay_payment.insert(ignore_permissions=True)
		
		razorpay_payment_status = frappe.db.get_value("Razorpay Payment", razorpay_payment_id, "status")
		
		self.assertEquals(razorpay_payment_status, "Authorized")
		
	def test_capture_payment(self):
		razorpay_settings = frappe.get_doc("Razorpay Settings")
		razorpay_settings.update(data["razorpay_settings"])
		
		razorpay_payment_id = "test_pay_{0}".format(frappe.generate_hash(length=14))
		
		razorpay_payment = make_payment(razorpay_payment_id=razorpay_payment_id,
			options=json.dumps(data["options"]))
			
		razorpay_payment.flags.is_sandbox = True
		razorpay_payment.sanbox_response = data["sanbox_response"]
		razorpay_payment.sanbox_response.update({
			"id": razorpay_payment_id,
			"status": "authorized"
		})
		
		razorpay_payment.insert(ignore_permissions=True)
		
		razorpay_payment.sanbox_response.update({
			"id": razorpay_payment_id,
			"status": "captured"
		})
		
		capture_payment(razorpay_payment_id=razorpay_payment_id ,is_sandbox=True,
			sanbox_response=razorpay_payment.sanbox_response)
		
		razorpay_payment_status = frappe.db.get_value("Razorpay Payment", razorpay_payment_id, "status")
		
		self.assertEquals(razorpay_payment_status, "Captured")
		
def make_payment(**args):
	args = frappe._dict(args)
	
	razorpay_payment = frappe.get_doc({
		"doctype": "Razorpay Payment",
		"razorpay_payment_id": args.razorpay_payment_id,
		"data": args.options
	})
	
	return razorpay_payment
	
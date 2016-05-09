# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
import json
from razorpay_integration.exceptions import InvalidRequest, AuthenticationError

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
	}
}

class TestRazorpayPayment(unittest.TestCase):
	def test_razorpay_settings(self):
		razorpay_settings = frappe.get_doc("Razorpay Settings")
		razorpay_settings.update(data["razorpay_settings"])
		self.assertRaises(AuthenticationError, razorpay_settings.insert)
	
	def test_confirm_payment(self):
		razorpay_payment = make_payment(razorpay_payment_id="pay_5U5aQI0vbky9M",
			options=json.dumps(data["options"]))
			
		self.assertRaises(InvalidRequest, razorpay_payment.insert)
	
	def test_capture_payment(self):
		pass

def make_payment(**args):
	args = frappe._dict(args)
	
	razorpay_payment = frappe.get_doc({
		"doctype": "Razorpay Payment",
		"razorpay_payment_id": args.razorpay_payment_id,
		"data": args.options
	})
	
	return razorpay_payment
	
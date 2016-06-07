# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

class AuthenticationError(Exception):
	http_status_code = 401
	
class GatewayError(Exception): 
	http_status_code = 500, 502, 504
	
class InvalidRequest(Exception):
	http_status_code = 400

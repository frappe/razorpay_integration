# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "razorpay_integration"
app_title = "Razorpay Integration"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = "Razorpay Payment Gateway Integration"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"
app_license = "MIT"
hide_in_installer = True
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/razorpay_integration/css/razorpay_integration.css"
# app_include_js = "/assets/razorpay_integration/js/razorpay_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/razorpay_integration/css/razorpay_integration.css"
# web_include_js = "/assets/razorpay_integration/js/razorpay_integration.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "razorpay_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "razorpay_integration.install.before_install"
# after_install = "razorpay_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "razorpay_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Payment Request": {
		"validate": "razorpay_integration.razorpay_integration.doctype.razorpay_settings.razorpay_settings.validate_razorpay_credentials",
		"get_payment_url": "razorpay_integration.utils.get_payment_url"
	},
	"Shopping Cart Settings": {
		"validate": "razorpay_integration.utils.validate_price_list_currency"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"razorpay_integration.razorpay_integration.doctype.razorpay_payment.razorpay_payment.authorise_payment",
		"razorpay_integration.razorpay_integration.doctype.razorpay_payment.razorpay_payment.capture_payment"
	]
}

# Testing
# -------

# before_tests = "razorpay_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "razorpay_integration.event.get_events"
# }


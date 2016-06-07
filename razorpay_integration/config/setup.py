from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Integrations"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Razorpay Settings",
					"description": _("Setup Razorpay credentials"),
					"hide_count": True
				}
			]
		}
	]
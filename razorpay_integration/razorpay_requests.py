from __future__ import unicode_literals
import frappe
from frappe.utils import get_request_session
from .exceptions import InvalidRequest, AuthenticationError, GatewayError

def get_request(url, auth=None):
	res = None
	if not auth:
		return

	try:
		s = get_request_session()
		res = s.get(url, data={}, auth=(auth.api_key, auth.api_secret))
		res.raise_for_status()
		return res.json()
	except Exception as exc:
		raise_exception(res, exc)

def post_request(url, data, auth=None):
	res = None

	if not auth:
		return

	try:
		s = get_request_session()
		res = s.post(url, data=data, auth=(auth.api_key, auth.api_secret))
		res.raise_for_status()
		return res.json()
	except Exception as exc:
		raise_exception(res, exc)

def raise_exception(res, exc):
	if hasattr(exc.args[0], "startswith"):
		if exc.args[0] and exc.args[0].startswith("400"):
			raise InvalidRequest(res.json().get("error", {}).get("description"))
		elif exc.args[0] and exc.args[0].startswith("401"):
			raise AuthenticationError(res.json().get("error", {}).get("description"))
		elif exc.args[0] and (exc.args[0].startswith("500") or exc.args[0].startswith("502") or exc.args[0].startswith("504")):
			raise GatewayError(res.json().get("error", {}).get("description"))
	else:
		frappe.throw(exc.message)
			

## Razorpay Integration

Razorpay Payment Gateway Integration with Frappe/ERPNext

### Usage

To get url for payment

1. Make a DocType for Order
2. On "pay now" button, redirect to razorpay_checkout page
3. When payment is authorized `on_payment_authorized` is called on the Order

### Example

#### "API"

```
from razorpay_integration.api import get_razorpay_checkout_url

@frappe.whitelist(allow_guest=True)
def make_payment(full_name, email, company, amount, workshop=None, conference=None):
	# make order
	participant = frappe.get_doc({
		'doctype': 'Conference Participant',
		'full_name': full_name,
		'email_id': email,
		'company_name': company,
		'workshop': workshop,
		'conference': conference,
		'amount': amount
	}).insert()

	# get razorpay url
	url = get_razorpay_checkout_url(**{
		'amount': amount,
		'title': 'ERPNext Conference Tickets',
		'description': '{0} passes for conference, {1} passes for workshop'.format(int(conference), int(workshop)),
		'payer_name': full_name,
		'payer_email': email,
		'doctype': participant.doctype,
		'name': participant.name,
		'order_id': participant.name
	})

	return url
```

#### when "Pay Now" is clicked

```
frappe.call({
	method: 'my_app.api.make_payment',
	args: data,
	callback: function(r) {
		// redirect to razor pay url
		window.location.href = r.message;
	}
});
```

#### Controller

```
class ConferenceParticipant(Document):
	def on_payment_authorized(self):
		self.db_set('paid', 1)
```

### License

MIT


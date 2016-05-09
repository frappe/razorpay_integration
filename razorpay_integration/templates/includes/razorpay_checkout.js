$(document).ready(function(){
	(function(e){
		var options = {
			"key": "{{ api_key }}",
			"amount": "{{ doc.grand_total }}" * 100, // 2000 paise = INR 20
			"name": "{{ company }}",
			"description": "{{ doc.subject }}",
			"image": "./assets/erpnext/images/erp-icon.svg",
			"handler": function (response){
				razorpay.make_payment_log(response, options, "{{ doc.doctype }}", "{{ doc.name }}");
			},
			"prefill": {
				"name": "{{ customer_name }}",
				"email": "{{ doc.email_to }}" || "{{ user }}",
				"contact": "9773595372",
				"order_id": "{{ doc.name }}",
			},
			"notes": {
				"payment_request": "{{ doc.name }}",
				"reference_doctype": "{{ doc.reference_doctype }}",
				"reference_docname": "{{ doc.reference_docname }}"
			},
			"theme": {
				"color": "#4B4C9D"
			}
		};
		
		var rzp = new Razorpay(options);
		rzp.open();
		//	e.preventDefault();
	})();
})

frappe.provide('razorpay');

razorpay.make_payment_log = function(response, options, doctype, docname){
	$('.razorpay-loading').addClass('hidden');
	$('.razorpay-confirming').removeClass('hidden');
	
	frappe.call({
		method:"razorpay_integration.templates.pages.razorpay_checkout.make_payment",
		freeze:true,
		headers: {"X-Requested-With": "XMLHttpRequest"},
		args: {
			"razorpay_payment_id": response.razorpay_payment_id,
			"options": options,
			"reference_doctype": doctype,
			"reference_docname": docname
		},
		callback: function(r){
			if (r.message && r.message.status == 200) {
				window.location.href = r.message.redirect_to
			}
		}
	})
}
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

version = '0.0.1'

setup(
	name='razorpay_integration',
	version=version,
	description='Razorpay Payment Gateway Integration',
	author='Frappe Technologies Pvt. Ltd.',
	author_email='info@frappe.io',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

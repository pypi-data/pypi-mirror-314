Burpy
=====


This module was created to parse and format the HTTP history from Burp Suite. The module was created to compensate for the ``Search`` and ``Save Project to Disk`` features which are missing from Burp Suite Community Edition. At the moment, ``Burpy`` can output to the following formats: xlsx, csv, json. 


Installation
------------


You can install ``burpy`` with ``pip``:
	$ pip install burpy


Usage
-----

In Python:
	>>> import burpy
	>>> burpy.log_analysis(file_path="PATH_TO_BURP_HTTP_HISTORY", output_format="csv")	

From commandline::
	$ burpy --file_path burp_logs --output_format csv


Changelog
---------


0.0.1 (2024-12-12)
******************
* Published initial version.
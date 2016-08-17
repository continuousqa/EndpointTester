## Endpoint Tester

This python 2.* script makes use of the module 'requests' so you'll need to have that installed prior:

pip install requests

## Usage

1. The script needs to be modified with your specific endpoints you're testing.

2. Once you modify them to your application's endpoints, then you need add data for each post you would normally do to yoru specific endpoints.

3. Replace a value you want to iterate over with XSS/SQL Injection, etc. with the value "evil" (examples are in the data.py)

Modify the script with bad data to suit your needs.

Tail the log files on your server while you put your endpoints through the test.
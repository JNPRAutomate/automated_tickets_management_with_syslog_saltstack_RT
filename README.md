# About RT

Request Tracker (RT) is an open source issue tracking system.  
RT REST API doc http://rt-wiki.bestpractical.com/wiki/REST  

# Docker 

There is a docker image available https://hub.docker.com/r/netsandbox/request-tracker/  
Use this command to pull it:  
```
# docker pull netsandbox/request-tracker
```
Validate you have the image using this command: 
```
# docker images
REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
netsandbox/request-tracker   latest              9943a8484f85        6 months ago        539MB
```
Use this command to instanciate a container:  
```
# docker run -d --rm --name rt -p 9081:80 netsandbox/request-tracker
cb68b252ee39514483b8885fe6e720de51f309c18a5fdca690bdad0258f715d0
```
use this command to list containers: 
```
# docker ps
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS                  PORTS                                                 NAMES
cb68b252ee39        netsandbox/request-tracker   "/usr/sbin/apache2..."   4 seconds ago       Up 3 seconds            0.0.0.0:9081->80/tcp                                  rt
```
# GUI

Access RT GUI with ```http://localhost:9081``` or ```http://host-ip:9081``` in a browser.  
The default ```root``` user password is ```password```  

# Python

There are python libraries that provide an easy programming interface for dealing with RT:  
- rtapi (https://github.com/Rickerd0613/rtapi) 
- python-rtkit (https://github.com/z4r/python-rtkit)
- rt (https://github.com/CZ-NIC/python-rt) 

## rt python library

Installation:  
```
# pip install -r requests nose six rt
```
Python interactive session demo: 
```
>>> import rt
>>> tracker = rt.Rt('http://172.30.52.150:9081/REST/1.0/', 'root', 'password')
>>> dir(tracker)
['RE_PATTERNS', '_Rt__check_response', '_Rt__correspond', '_Rt__get_status_code', '_Rt__normalize_list', '_Rt__request', '__doc__', '__init__', '__module__', 'comment', 'create_queue', 'create_ticket', 'create_user', 'default_login', 'default_password', 'default_queue', 'edit_link', 'edit_queue', 'edit_ticket', 'edit_ticket_links', 'edit_user', 'get_attachment', 'get_attachment_content', 'get_attachments', 'get_attachments_ids', 'get_history', 'get_links', 'get_queue', 'get_short_history', 'get_ticket', 'get_user', 'last_updated', 'login', 'login_result', 'logout', 'merge_ticket', 'new_correspondence', 'reply', 'search', 'session', 'steal', 'take', 'untake', 'url']
>>> tracker.url
'http://172.30.52.150:9081/REST/1.0/'
>>> tracker.login()
True
>>> tracker.search(Queue='General', Status='new')
[{u'Status': u'new', u'Priority': u'0', u'Resolved': u'Not set', u'TimeLeft': u'0', u'Creator': u'root', u'Started': u'Not set', u'Starts': u'Not set', u'Created': u'Mon May 14 07:54:23 2018', u'Due': u'Not set', u'LastUpdated': u'Mon May 14 07:54:25 2018', u'FinalPriority': u'0', u'Queue': u'General', 'Requestors': [u''], u'Owner': u'Nobody', u'Told': u'Not set', u'TimeEstimated': u'0', u'InitialPriority': u'0', u'id': u'ticket/1', u'TimeWorked': u'0', u'Subject': u'Device 172.30.52.85 configuration is not inline with the golden configuration rules described in test_telnet.yml'}, {u'Status': u'new', u'Priority': u'0', u'Resolved': u'Not set', u'TimeLeft': u'0', u'Creator': u'root', u'Started': u'Not set', u'Starts': u'Not set', u'Created': u'Tue May 15 06:58:38 2018', u'Due': u'Not set', u'LastUpdated': u'Tue May 15 06:58:40 2018', u'FinalPriority': u'0', u'Queue': u'General', 'Requestors': [u''], u'Owner': u'Nobody', u'Told': u'Not set', u'TimeEstimated': u'0', u'InitialPriority': u'0', u'id': u'ticket/2', u'TimeWorked': u'0', u'Subject': u'Device 172.30.52.85 configuration is not inline with the golden configuration rules described in test_telnet.yml'}]
>>> for item in tracker.search(Queue='General', Status='new'):
...     print item['id']
...
ticket/1
ticket/2
>>> tracker.create_ticket(Queue='General', Subject='abc', Text='bla bla bla')
4
>>> tracker.edit_ticket(4, Priority=3)
True
>>> tracker.reply(4, text='Do you know Starbucks???')
True
>>> tracker.logout()
True
```

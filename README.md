# About this project 

Junos automation demo using SaltStack and a ticketing system (Request Tracker). 

## Demo overview  
- Junos devices send syslog messages to SaltStack.  
- SaltStack automatically creates a new ticket (or update an existing ticket) using RT (Request Tracker) 

## Demo building blocks 
- Junos  devices
- SaltStack
- RT (Request Tracker) 

## Building blocks role 

### Request Tracker 
- This is the ticketing system. The tickets are automatically created and updated by SaltStack based on Junos syslog messages. 

### Junos devices
- They send syslog messages to SaltStack

### SaltStack  
- The Salt master listens to syslog messages sent by junos devices
- The Salt master generates a ZMQ message to the event bus when a junos syslog message is received. The ZMQ message has a tag and data. The data structure is a dictionary, which contains information about the event.
- The Salt reactor binds sls files to event tags. The reactor has a list of event tags to be matched, and each event tag has a list of reactor SLS files to be run. So these sls files define the SaltStack reactions.
- The sls reactor file used in this content does the following: it parses the data from the ZMQ message to extract data (the network device name, and additional details). It then passes the data extracted to a runner (python script).  
- The runner creates a new ticket (or update an existing ticket) using RT (Request Tracker) 

# Request Tracker 

Request Tracker (RT) is an open source issue tracking system.  
RT REST API doc http://rt-wiki.bestpractical.com/wiki/REST  

## install RT

There is a docker image available https://hub.docker.com/r/netsandbox/request-tracker/  
Pull the image: 
```
# docker pull netsandbox/request-tracker
```
Verify: 
```
# docker images
REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
netsandbox/request-tracker   latest              9943a8484f85        6 months ago        539MB
```
Instanciate a container: 
```
# docker run -d --rm --name rt -p 9081:80 netsandbox/request-tracker
cb68b252ee39514483b8885fe6e720de51f309c18a5fdca690bdad0258f715d0
```
Verify:
```
# docker ps
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS                  PORTS                                                 NAMES
cb68b252ee39        netsandbox/request-tracker   "/usr/sbin/apache2..."   4 seconds ago       Up 3 seconds            0.0.0.0:9081->80/tcp                                  rt
```


## RT GUI
Access RT GUI with ```http://localhost:9081``` or ```http://host-ip:9081``` in a browser.  
The default ```root``` user password is ```password```  

## Python libraries for RT 

There are python libraries that provide an easy programming interface for dealing with RT:  
- [rtapi](https://github.com/Rickerd0613/rtapi) 
- [python-rtkit](https://github.com/z4r/python-rtkit)
- [rt](https://github.com/CZ-NIC/python-rt) 

Install the rt library
```
# pip install -r requests nose six rt
```
```
# pip list
```
Verify using a python interactive session:
```
# python
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
>>> tracker.reply(4, text='Write here the notes you want to add to the ticket')
True
>>> tracker.logout()
True
```
# SaltStack

## Install SaltStack

This is not covered by this documentation.

## Install the rt python library 
```
# pip install -r requests nose six rt
```

## Update the master configuration file

Edit the salt master configuration file:  
```
vi /etc/salt/master
```
Make sure the master configuration file has these details:  
```
runner_dirs:
  - /srv/runners
```
```
engines:
  - junos_syslog:
      port: 516
```
```
ext_pillar:
  - git:
    - master git@gitlab:organization/network_parameters.git
```

So: 
- The runners are in the directory ```/srv/runners``` on the master
- the Salt master is listening junos syslog messages on port 516. For each junos syslog message received, it generates an equivalent ZMQ message and publish it to the event bus
- external pillars (variables) are in the gitlab repository ```organization/network_parameters``` (master branch)


## Update the pillars 

Update the pillars with the required rt details.  
[Here's an example](rt_pillars.sls)

Verify:  
```
# salt-run pillar.show_pillar
```

## Update the runners 

Add this [file](request_tracker_saltstack_runner.py) to your runners

Then, test your runner manually from the master: 
```
salt-run request_tracker_saltstack_runner.create_ticket subject='test' text='test text'
```
```
salt-run request_tracker_saltstack_runner.change_ticket_status_to_resolved ticket_id=1
```
## Update the reactor configuration file

The reactor binds sls files to event tags. The reactor has a list of event tags to be matched, and each event tag has a list of reactor SLS files to be run. So these sls files define the SaltStack reactions.  

Update your reactor configuration file.  
[Here's an example](reactor.conf). This reactor configuration file binds ```jnpr/syslog/*/SNMP_TRAP_LINK_*``` to ```/srv/reactor/create_interface_status_change_ticket.sls```  

Restart the Salt master:
```
service salt-master stop
service salt-master start
```
This command lists currently configured reactors:  
```
salt-run reactor.list
```

## Update the sls files
Create the sls file that will be fired automatically by the reactor.  
[Here's an example](create_interface_status_change_ticket.sls)  


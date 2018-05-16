import rt
import salt.runner

def get_rt_pillars():
    opts = salt.config.master_config('/etc/salt/master')
    runner = salt.runner.RunnerClient(opts)
    pillar = runner.cmd('pillar.show_pillar')
    uri = pillar['rt']['uri']
    username = pillar['rt']['username']
    password = pillar['rt']['password']
    return {'uri': uri, 'username': username, 'password': password}

def connect_to_rt():
   rt_pillars=get_rt_pillars()
   uri = rt_pillars['uri']
   username = rt_pillars['username']
   password = rt_pillars['password']
   tracker = rt.Rt(uri, username, password)
   tracker.login()
   return tracker

def check_if_a_ticket_already_exist(subject):
   tracker=connect_to_rt()
   ticket_already_exist = False
   for item in tracker.search(Queue='General'):
       if item['Subject'] == subject:
           ticket_already_exist = True
           id=str(item['id']).split('/')[-1]
       if ticket_already_exist:
           tracker.logout()
           return id
       else:
           tracker.logout()
           return False

def create_ticket(subject, text):
    tracker=connect_to_rt()
    if check_if_a_ticket_already_exist(subject) == False:
        ticket_id = tracker.create_ticket(Queue='General', Subject=subject, Text=text)
        tracker.logout()
        return ticket_id
    else:
        ticket_id = check_if_a_ticket_already_exist(subject)
        update_ticket(ticket_id, text)
        tracker.logout()
        return ticket_id

def update_ticket(ticket_id, text):
    tracker=connect_to_rt()
    tracker.reply(ticket_id, text=text)
    tracker.logout()


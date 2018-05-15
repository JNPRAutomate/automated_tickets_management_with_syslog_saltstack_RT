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

def create_ticket(subject, text):
    rt_pillars=get_rt_pillars()
    uri = rt_pillars['uri']
    username = rt_pillars['username']
    password = rt_pillars['password']
    tracker = rt.Rt(uri, username, password)
    tracker.login()
    ticket_id = tracker.create_ticket(Queue='General', Subject=subject, Text=text)
    tracker.logout()
    return ticket_id

def update_ticket(ticket_id, text):
    rt_pillars=get_rt_pillars()
    uri = rt_pillars['uri']
    username = rt_pillars['username']
    password = rt_pillars['password']
    tracker = rt.Rt(uri, username, password)
    tracker.login()
    tracker.reply(ticket_id, text=text)
    tracker.logout()

# ticket_id = create_ticket('subject_example', 'text_example')  
# update_ticket(ticket_id, 'text_update')

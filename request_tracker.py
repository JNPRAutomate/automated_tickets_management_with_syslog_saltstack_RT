import rt

uri = 'http://172.30.52.150:9081/REST/1.0/'
username = 'root'
password = 'password'

def create_ticket(subject, text):
    tracker = rt.Rt(uri, username, password)
    tracker.login()
    ticket_id = tracker.create_ticket(Queue='General', Subject=subject, Text=text)
    tracker.logout()
    return ticket_id

def update_ticket(ticket_id, text):
    tracker = rt.Rt(uri, username, password)
    tracker.login()
    tracker.reply(ticket_id, text=text)
    tracker.logout()

ticket_id = create_ticket('subject_example', 'text_example')  
update_ticket(ticket_id, 'text_update')

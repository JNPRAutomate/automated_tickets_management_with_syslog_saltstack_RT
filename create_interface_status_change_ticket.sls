```
# more /srv/reactor/create_interface_status_change_ticket.sls
{% if data['data'] is defined %}
{% set d = data['data'] %}
{% else %}
{% set d = data %}
{% endif %}
{% set interface = d['message'].split(' ')[-1] %}
{% set interface = interface.split('.')[0] %}
create a ticket:
  runner.request_tracker_saltstack_runner.create_ticket:
    - kwarg:
        subject: "device {{ d['hostname'] }} had its interface {{ interface }} status that changed"
        text: " {{ d['message'] }}"

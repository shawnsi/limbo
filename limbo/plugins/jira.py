import os
import re
import requests

def jira(issue_key):

    jira_user = os.environ['JIRA_USER']
    jira_password = os.environ['JIRA_PASSWORD']
    jira_url = os.environ['JIRA_URL']
    print '%s/rest/api/2/issue/%s' % (jira_url, issue_key)

    results = requests.get(('%srest/api/2/issue/%s' % (jira_url, issue_key)), auth=(jira_user, jira_password))

    issue = results.json
    ticket_url = "https://jira.meredith.com/dt/browse/%s\n" % issue_key
    ticket_status = "Ticket Status: %s\n" % (issue()['fields']['status']['name'])
    ticket_assignee = "Ticket Assignee: %s\n" % (issue()['fields']['assignee']['name'])
    ticket_creator = "Ticket Creator: %s\n" % (issue()['fields']['creator']['name'])
    ticket_summary = "%s - %s\n" % (issue_key, issue()['fields']['summary'])

    response = ticket_url + ticket_summary + ticket_status + ticket_creator + ticket_assignee
    return response


def on_message(msg, server):
    text = msg.get("text", "")
    issue_key = re.findall(r"!jira\ (.*)", text)
    if not issue_key:
        return

    return jira(issue_key[0])

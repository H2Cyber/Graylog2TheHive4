from __future__ import print_function
from __future__ import unicode_literals
import sys
import requests
import json
import time
import uuid
import logging
import re
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper
from flask import Flask, Response, render_template, request, flash, redirect, url_for

app = Flask(__name__)

# Configure TheHiveAPI URL and API code here
# Exmaple : api = TheHiveApi('http://127.0.0.1:9000', 'HYEOKSYEHZFSQHZYTSRF')
api = TheHiveApi('http://127.0.0.1:9000', 'YOUR-API-KEY')

# Configure Graylog URL here
# Exmaple : graylog_url = 'http://10.10.10.10:9000'
graylog_url = 'http://YOUR-GRAYLOG-IP:9000'

# Webhook to process Graylog HTTP Notification
@app.route('/webhook', methods=['POST'])
def webhook():

    # Get request JSON contents
    content = request.get_json()
    event = content['event']

    # Configure Alert tags
    tags = ['Graylog']

    # Configure Alert title
    title = event['message']

    # Configure Alert description
    description = "**Graylog event definition:** "+content['event_definition_title']
    if content['backlog']:
        description = description+'\n\n**Matching messages:**\n\n'
        for message in content['backlog']:
            description = description+"\n\n---\n\n**Graylog URL:** "+graylog_url+"/messages/"+message['index']+"/"+message['id']+"\n\n"
            description = description+'\n\n**Raw Message:** \n\n```\n'+json.dumps(message)+'\n```\n---\n'

    # Configure Alert severity
    severity = event['priority']

    # Extract IP from Graylog event and configure it as an Alert artificat
    artifacts = []
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    if ip_pattern.search(event['message']):
      ip = ip_pattern.search(event['message'])[0]
      artifacts = [AlertArtifact(dataType='ip', data=ip)]
    else:
      groupby_pattern = re.compile(r'\:\s(.*)\s-')
      if groupby_pattern.search(event['message']):
        groupby = groupby_pattern.search(event['message'])[0]
        artifacts = [AlertArtifact(dataType='other', data=groupby)]


    # Prepare the Alert
    sourceRef = str(uuid.uuid4())[0:6]
    alert = Alert(title=title,
                  tlp=2,
                  tags=tags,
                  description=description,
                  severity=severity,
                  artifacts=artifacts,
                  type='external',
                  source='Graylog',
                  sourceRef=sourceRef)

    # Create the Alert
    print('Creating alert for: '+title)
    response = api.create_alert(alert)
    if response.status_code == 201:
        print('Alert created successfully for: '+title)
    else:
        print('Error while creating alert for: '+title)
        sys.exit(0)
    return content['event_definition_title']

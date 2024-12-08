import requests
import json
import os
def pyInstantSend(webhookURL, message, displayName=None):
    if displayName != None:
        stupid = {'content': message, 'username': displayName}
        requests.post(webhookURL,stupid)
    else:
        stupid = {'content': message}
        requests.post(webhookURL,stupid)
def pySend():
    webhookURL = input('What is the webhook URL? ')
    message = input('Type in your message. ')
    messageToJSON = {'content': message}
    requests.post(webhookURL,messageToJSON)
pyInstantSend('https://discord.com/api/webhooks/1309344069041782814/n7dzgVqdZB05a3_LVPmGeWQfBCgaglX9mJDv-PDHGbp_y8cpWI-2b1AICXi1ScKaaYrI', 'Demon.')
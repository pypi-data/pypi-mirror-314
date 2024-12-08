# PyLaysWebhooker
A discord webhook program i made based off my webhooker site https://layswebhooker.vercel.app
You're gonna need requests module to install this module.
```
pip install requests
```
Basically i made this for discord webhook message sending to be easier for others, like Discohook.
Here is an example of a code to send a webhook message in the console
```
import pyLaysWebhooker
pyLaysWebhooker.pySend()
```
Here is another example but to instantly send a message as soon as the example is ran in Python.
```
import pyLaysWebhooker
pyLaysWebhooker.pyInstantSend('WEBHOOK_URL','Hi, my name is Lays Webhook.', 'Lays Webhook')
```
Don't worry, the 3rd argument in pyInstantSend() is optional. Everything else is required though.
To send an image with the Lays Webhooker, you need to have a link that represents the image in the message.
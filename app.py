'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>
`
Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import os
import base64
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import datetime, sys
import requests
import json

if sys.version_info >= (3, 0):
	raw_input = input

from Yowsup.connectionmanager import YowsupConnectionManager

class WhatsappListenerClient:
	
	def __init__(self, keepAlive = False, sendReceipts = False):
		self.sendReceipts = sendReceipts
		
		connectionManager = YowsupConnectionManager()
		connectionManager.setAutoPong(keepAlive)

		self.signalsInterface = connectionManager.getSignalsInterface()
		self.methodsInterface = connectionManager.getMethodsInterface()	
		self.signalsInterface.registerListener("receipt_messageSent",self.onMessageSent)
		self.signalsInterface.registerListener("receipt_messageDelivered", self.onMessageDelivered)
		self.signalsInterface.registerListener("message_received", self.onMessageReceived)
		self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
		self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
		self.signalsInterface.registerListener("disconnected", self.onDisconnected)		
#		self.cm = connectionManager
		
	def login(self, username, password):
		self.username = username
		self.methodsInterface.call("auth_login", (username, password))
		
		
		#while True:
		#	raw_input()	

	def onAuthSuccess(self, username):
		print("Authed %s" % username)
		self.methodsInterface.call("ready")

	def onAuthFailed(self, username, err):
		print("Auth Failed!")

	def onDisconnected(self, reason):
		print("Disconnected because %s" %reason)

	def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadCast):
		formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
		print("%s [%s]:%s"%(jid, formattedDate, messageContent))
		print jid
		payload = {"message": {"content":" + messageContent + ", \"phone\":" + jid +" } }"
		#payload = {"message": {"content": "ativo", "phone": "18298647935@s.whatsapp.net"}}
		requests.post('http://localhost:3000/messages', data=payload)
		if wantsReceipt and self.sendReceipts:
			self.methodsInterface.call("message_ack", (jid, messageId))
	

	def onMessageSent(jid, messageId):
		print "Message was sent successfully to %s" % jid

	def onMessageDelivered(jid, messageId):
		print "Message was delivered successfully to %s" %jid
		methodsInterface.call("delivered_ack", (jid, messageId))

		# First we init the whatsapp listener

listener = WhatsappListenerClient()

password = 'NzWbfEQHv+4HvFtLKppjYQ49cVM='
vUsername = '18097800487'
vBase64Pwd = base64.b64decode(bytes(password.encode('utf-8')))
listener.login(username=vUsername,password=vBase64Pwd)


from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource, request

messages = {}

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

@app.route ('/')

# For sending messages
class WpSend(Resource):
	def post(self):
		json = request.json
		msg = json['msg']
		msg = msg.encode('ascii', 'ignore')
		numb = json['number']
		numb = numb.encode('ascii','ignore')
		listener.methodsInterface.call("message_send", (numb + "@s.whatsapp.net", msg )) 
		print ("Sended: " + msg + " To: " + numb)

# For storing and showing messages
class WpMsg(Resource):
	def post(self,numb):
		json = request.json
		msg = json['msg']
		msg = msg.encode('ascii', 'ignore')
		numb = numb
#		numb = num.encode('ascii', 'ignore')
		messages[numb] = msg
	
	def get(self, numb ):
		return { numb : messages[numb] }

api.add_resource(WpSend,'/message')
api.add_resource(WpMsg,'/<string:numb>')

if __name__ == '__main__':
	app.run(debug=True)


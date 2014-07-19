Sarah-Whatsapp connection module

To send message to a number via post

curl -H "Content-Type: application/json" -d '{ "msg":"Como estas", "number": " phone number"}' http://localhost:5000/message

Received messages are sent to server:

http://localhost:3000/messages

with json: {"message": {"content": messageContent, "phone": jid } }



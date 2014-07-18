from flask import Flask
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

mesg = {}

class WhatsAppCom(Resource):
	def get(self, mesg_id):
		return {mesg_id: mesg[mesg_id] }
	def put(self, mesg_id):
		mesg[mesg_id] = request.form['data']
		return { mesg_id: mesg[mesg_id] } 

api.add_resource(WhatsAppCom, '/<string:mesg_id>')

if __name__ == '__main__':
	app.run(debug=True)




from flask import Flask
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class WhatsAppCom(Resource):
	def get(self):
		return {'mesg_id': "connecting" }
	def post(self):
		args = parser.parser_args()
		mesg_id = {'sended' : args['message']}
	return mesg_id, 201
		
api.add_resource(WhatsAppCom, '/<string:mesg_id>')

if __name__ == '__main__':
	app.run(debug=True)



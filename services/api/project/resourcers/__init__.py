from flask_restful import Resource


class Alive(Resource):
	def __init__(self):
		pass
	def get(self):
		return {"message": "alive", "status": "success"}


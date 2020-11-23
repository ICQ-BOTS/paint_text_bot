import tarantool

connection = tarantool.connect("localhost", 3303)

space_user = connection.space('user')

 
class User:
	def __init__(self, user_id,):
		self.user = space_user.select(user_id)
		self.user_id = user_id

	def get(self):
		if not self.user:
			self.user = space_user.insert((self.user_id, True, {'text': None}))
		
		self.space = self.user[0]
		self.old_mes = self.space[2]
		return self

	def save(self):
		space_user.replace(self.user[0])   
 
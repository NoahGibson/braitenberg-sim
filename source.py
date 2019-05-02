# Source canvas object to display
class Source:

	# Constructor
	def __init__(self, canvas, x, y):
		self.radius = 8
		self.canvas = canvas
		self.x = x
		self.y = y
		self.source = self.canvas.create_oval(
			x-self.radius,
			y-self.radius,
			x+self.radius,
			y+self.radius,
			fill='#FFFFFF')

	# Deletes the canvas display of the source
	def destroy(self):
		self.canvas.delete(self.source)

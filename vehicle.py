# Imports
import math
import numpy as np

# Vehicle canvas object and controller
class Vehicle:

	# Contructor
	def __init__(self, parent, canvas, x, y):
		self.canvas = canvas
		self.environment = parent
		self.x = x
		self.y = y
		self.speedRatio = 0.15 # The conversion rate between the input sensor amount and the speed of the wheel
		self.width = 30
		self.height = 20
		self.maxSpeed = 1
		self.maxSensor = 300

		# The vertices of the vehicle drawing
		self.vertices = [
			[self.x - self.width/2, self.y - self.height/2],
			[self.x + self.width/2, self.y - self.height/2],
			[self.x + self.width/2, self.y + self.height/2],
			[self.x + self.width/4 + 2, self.y + self.height/2],
			[self.x + self.width/4 + 2, self.y + self.height/2 + 2],
			[self.x + self.width/4 - 2, self.y + self.height/2 + 2],
			[self.x + self.width/4 - 2, self.y + self.height/2],
			[self.x - self.width/4 + 2, self.y + self.height/2],
			[self.x - self.width/4 + 2, self.y + self.height/2 + 2],
			[self.x - self.width/4 - 2, self.y + self.height/2 + 2],
			[self.x - self.width/4 - 2, self.y + self.height/2],
			[self.x - self.width/2, self.y + self.height/2]
		]

		# The sensors of the vehicle
		self.lSensor = {
			'x': self.x + self.width/4,
			'y': self.y + self.height/2,
			'inhibitory': False,
			'attachment': 'left'
		}
		self.rSensor = {
			'x': self.x - self.width/4,
			'y': self.y + self.height/2,
			'inhibitory': False,
			'attachment': 'right'
		}

		# The wheels of the vehicle
		self.lWheel = {
			'x': self.x + self.width/2,
			'y': self.y,
			'inhibitory': False,
		}
		self.rWheel = {
			'x': self.x - self.width/2,
			'y': self.y,
			'inhibitory': False,
		}

		# Rendering the vehicle drawing initially
		self.render()

	# Processes the given inputs for the two sensors of the vehicle, specifically, moving the 
	# vehicle for the given sensor inputs
	def processInput(self, rightInput, leftInput, duration):
		
		# Setting constant t to the duration of the movement
		t = duration

		# Getting the speed of each wheel, and their average speed
		vRight = 0
		vLeft = 0
		iRight = rightInput
		iLeft = leftInput
		# Changing inputs if inhibitory
		if self.rSensor['inhibitory']:
			iRight = self.maxSensor - iRight
		if self.lSensor['inhibitory']:
			iLeft = self.maxSensor - iLeft
		# Getting the velocity from the corresponding sensors
		if self.rSensor['attachment'] == 'right':
			vRight += self.speedRatio * iRight
		else:
			vLeft += self.speedRatio * iRight
		if self.lSensor['attachment'] == 'left':
			vLeft += self.speedRatio * iLeft
		else:
			vRight += self.speedRatio * iLeft
		# Maxing out the speed of each wheel
		vRight = vRight if vRight < self.maxSpeed else self.maxSpeed
		vLeft = vLeft if vLeft < self.maxSpeed else self.maxSpeed
		# Changing velocity if inhibitory
		if self.rWheel['inhibitory']:
			vRight = self.maxSpeed - vRight
		if self.lWheel['inhibitory']:
			vLeft = self.maxSpeed - vLeft
		# Getting average of velocities
		vAvg = (vRight + vLeft) / 2

		# If the speeds are not equal, vehicle will rotate
		if (vRight != vLeft):

			# Get the length of the radius of the vehicle's rotation
			turnRadius = 0.5 * self.width if vRight == 0 else (0.5 * self.width + self.width/((vLeft/vRight) - 1))

			# Getting the angular velocity of the car
			omega = vAvg / turnRadius

			# Getting the angle through which the vehicle will rotate
			theta = omega * t

			# Getting the center around which the vehicle will rotate
			v = np.array([self.rWheel['x'] - self.x, self.rWheel['y'] - self.y])
			u = v / np.linalg.norm(v)
			xTurn, yTurn = np.array([self.x, self.y]) + turnRadius * u
			
			# Rotating the vehicle
			self.rotate(xTurn, yTurn, theta)

		# If speeds are equal, vehicle will move forward
		else:

			# Getting the distance that the vehicle will travel forward
			distance = vAvg * t

			# Getting the amount the vehicle should move
			direction = np.array([self.rWheel['y'] - self.y, -(self.rWheel['x'] - self.x)])
			direction = direction / np.linalg.norm(direction)
			xTrans, yTrans = distance * direction

			# Moving the vehicle
			self.translate(xTrans, yTrans)

	# Rotates the car around the given point through the given angle (angle should be in radians)
	def rotate(self, x, y, angle):

		# Getting the sine and cosine of the angle
		cosVal = math.cos(angle)
		sinVal = math.sin(angle)

		# Updating drawing vertices
		newVertices = []
		for vertex in self.vertices:
			xOld = vertex[0] - x
			yOld = vertex[1] - y
			xNew = xOld * cosVal - yOld * sinVal
			yNew = xOld * sinVal + yOld * cosVal
			newVertices.append([xNew + x, yNew + y])
		self.vertices = newVertices

		# Updating car center
		oldX = self.x - x
		oldY = self.y - y
		self.x = oldX * cosVal - oldY * sinVal + x
		self.y = oldX * sinVal + oldY * cosVal + y

		# Updating sensor locations
		oldLSX = self.lSensor['x'] - x
		oldLSY = self.lSensor['y'] - y
		oldRSX = self.rSensor['x'] - x
		oldRSY = self.rSensor['y'] - y
		self.lSensor['x'] = oldLSX * cosVal - oldLSY * sinVal + x
		self.lSensor['y'] = oldLSX * sinVal + oldLSY * cosVal + y
		self.rSensor['x'] = oldRSX * cosVal - oldRSY * sinVal + x
		self.rSensor['y'] = oldRSX * sinVal + oldRSY * cosVal + y

		# Updating wheel locations
		oldLWX = self.lWheel['x'] - x
		oldLWY = self.lWheel['y'] - y
		oldRWX = self.rWheel['x'] - x
		oldRWY = self.rWheel['y'] - y
		self.lWheel['x'] = oldLWX * cosVal - oldLWY * sinVal + x
		self.lWheel['y'] = oldLWX * sinVal + oldLWY * cosVal + y
		self.rWheel['x'] = oldRWX * cosVal - oldRWY * sinVal + x
		self.rWheel['y'] = oldRWX * sinVal + oldRWY * cosVal + y

		# Removing old drawing and making new one
		self.destroy()
		self.render()

	# Translates the car so that its center is moved by the given x and y amount 
	def translate(self, x, y):

		# Updating drawing vertices
		newVertices = []
		for vertex in self.vertices:
			newVertices.append([vertex[0] + x, vertex[1] + y])
		self.vertices = newVertices

		# Updating car center
		self.x = self.x + x
		self.y = self.y + y

		# Updating sensor locations
		self.lSensor['x'] = self.lSensor['x'] + x
		self.lSensor['y'] = self.lSensor['y'] + y
		self.rSensor['x'] = self.rSensor['x'] + x
		self.rSensor['y'] = self.rSensor['y'] + y

		# Updating wheel locations
		self.lWheel['x'] = self.lWheel['x'] + x
		self.lWheel['y'] = self.lWheel['y'] + y
		self.rWheel['x'] = self.rWheel['x'] + x
		self.rWheel['y'] = self.rWheel['y'] + y

		# Removing old drawing and making new one
		self.destroy()
		self.render()

	# Moves the vehicle's center to the given point
	def moveTo(self, x, y):

		# Updating drawing vertices
		newVertices = []
		for vertex in self.vertices:
			xDif = vertex[0] - self.x
			yDif = vertex[1] - self.y
			newVertices.append([x + xDif, y + yDif])
		self.vertices = newVertices

		# Updating sensor locations
		xLSDif = self.lSensor['x'] - self.x
		yLSDif = self.lSensor['y'] - self.y
		xRSDif = self.rSensor['x'] - self.x
		yRSDif = self.rSensor['y'] - self.y
		self.lSensor['x'] = xLSDif + x
		self.lSensor['y'] = yLSDif + y
		self.rSensor['x'] = xRSDif + x
		self.rSensor['y'] = yRSDif + y

		# Updating wheel locations
		xLWDif = self.lWheel['x'] - self.x
		yLWDif = self.lWheel['y'] - self.y
		xRWDif = self.rWheel['x'] - self.x
		yRWDif = self.rWheel['y'] - self.y
		self.lWheel['x'] = xLWDif + x
		self.lWheel['y'] = yLWDif + y
		self.rWheel['x'] = xRWDif + x
		self.rWheel['y'] = yRWDif + y

		# Updating car center
		self.x = x
		self.y = y

		# Removing old drawing and making new one
		self.destroy()
		self.render()

	# Deletes the canvas display of the vehicle
	def destroy(self):
		self.canvas.delete(self.drawing)

	# Renders the canvas display of the vehicle
	def render(self):
		self.drawing = self.canvas.create_polygon(self.vertices, fill='#FFFFFF')

	# Sets the attachment wheel for the left sensor
	def setLeftSensorAttachment(self, wheel):
		if wheel != 'left' and wheel != 'right':
			raise ValueError('wheel must be either "left" or "right", but got ' + str(wheel))
		self.lSensor['attachment'] = wheel

	# Sets the attachment wheel for the right sensor
	def setRightSensorAttachment(self, wheel):
		if wheel != 'left' and wheel != 'right':
			raise ValueError('wheel must be either "left" or "right", but got ' + str(wheel))
		self.rSensor['attachment'] = wheel

	# Sets the inibition for the left sensor
	def setLeftSensorInhibit(self, inhibit):
		self.lSensor['inhibitory'] = inhibit

	# Sets the inibition for the right sensor
	def setRightSensorInhibit(self, inhibit):
		self.rSensor['inhibitory'] = inhibit

	# Sets the inibition for the left wheel
	def setLeftWheelInhibit(self, inhibit):
		self.lWheel['inhibitory'] = inhibit

	# Sets the inibition for the right wheel
	def setRightWheelInhibit(self, inhibit):
		self.rWheel['inhibitory'] = inhibit

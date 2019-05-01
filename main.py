#!/usr/bin/env python

'''
Braitenberg Vehicle Simulator Application

A simple GUI application that allows users to create simple Braitenberg vehicles
and view their behavior within an environment.

Author: Noah Gibson
Updated: 20190501

'''

# GLOBAL VARIABLES -----------------------------------------------------------------------------------

# The name of the app
APP_NAME = 'Braitenberg Vehicle Simulator'

# The background color of the app
BACKGROUND_COLOR = '#220011'

# The text color for the app
TEXT_COLOR = '#FFFFFF'

# The application object
app = None


# IMPORTS --------------------------------------------------------------------------------------------

# Import math for calculations
import math

# Import Tkinter for GUI handling
import tkinter as tk
from tkinter import messagebox

# Import NumPy for linear algebra calculations
import numpy as np


# CLASSES --------------------------------------------------------------------------------------------

# Header for the content of the app
class ContentHeader(tk.Frame):

	# Constructor
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.headerLabel = tk.Label(
			self,
			justify=tk.CENTER,
			text=APP_NAME,
			font='Helvetica 24',
			fg=TEXT_COLOR,
			bg=self.parent['bg'],
			pady=30)
		self.headerLabel.pack()


# Form for interacting with the app
class ContentForm(tk.Frame):

	# Constructor
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.config(bg=self.parent['bg'])
		self.initForm()

	# Initializes the form
	def initForm(self):
		entryBgColor = '#333333'
		entryFgColor = '#FFFFFF'
		font = 'Helvetica 12'

		# Add source label
		addSourceLabel = tk.Label(
			self,
			text='Add Source',
			font='Helvetica 14 bold',
			fg=TEXT_COLOR,
			bg=self.parent['bg'])
		addSourceLabel.grid(row=0, column=0, columnspan=5, sticky='w', pady=5)

		# Source X index label
		sourceXLabel = tk.Label(self, text='Column:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		sourceXLabel.grid(row=1, column=2, padx=5)

		# Source X index entry
		self.sourceX = tk.Entry(self, width=5, font=font, bg=entryBgColor, fg=entryFgColor, justify=tk.CENTER)
		self.sourceX.grid(row=1, column=3, padx=5)

		# Source Y index label
		sourceYLabel = tk.Label(self, text='Row:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		sourceYLabel.grid(row=1, column=0, padx=5)

		# Source Y index entry
		self.sourceY = tk.Entry(self, width=5, font=font, bg=entryBgColor, fg=entryFgColor, justify=tk.CENTER)
		self.sourceY.grid(row=1, column=1, padx=5)

		# Add Source confirm
		sourceConfirm = tk.Button(self, text='Add Source', width=20, font='Helvetica 10 bold', command=self.addSource)
		sourceConfirm.grid(row=1, column=4, padx=20)

		# Edit Vehicle label
		editLeftSensor = tk.Label(
			self,
			text='Edit Left Sensor',
			font='Helvetica 14 bold',
			fg=TEXT_COLOR,
			bg=self.parent['bg'])
		editLeftSensor.grid(row=2, column=0, columnspan=5, sticky='w', pady=(10, 5))

		# Left sensor attachment Label
		lSAttachLabel = tk.Label(self, text='Attachment:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		lSAttachLabel.grid(row=3, column=0, padx=5)

		# Left sensor attachment
		self.lSAttach = tk.Entry(self, width=7, font=font, bg=entryBgColor, fg=entryFgColor)
		self.lSAttach.grid(row=3, column=1, padx=5)

		# TODO - Add vehicle params form

		# Run the simulation
		self.runSimBtn = tk.Button(self, text='Run Simulation', font='Helvetica 14 bold', width=30, command=self.runSimulation)
		self.runSimBtn.grid(row=5, column=0, columnspan=5, pady=(30, 10))

		# Reset the sources and vehicle
		self.resetBtn = tk.Button(self, text='Reset', font='Helvetica 10 bold', width=7, command=self.resetEnv)
		self.resetBtn.grid(row=6, column=0, columnspan=5, pady=(10, 20))

	# Retrieves the currently entered values for the source addition and adds it to the environment state
	def addSource(self):
		try:
			xIndex = int(self.sourceX.get())
			if xIndex < 0 or xIndex > 6:
				raise ValueError()
		except ValueError:
			messagebox.showwarning('Invalid Column', 'The column value must be an integer between 0 and 6.')
			return
		try:
			yIndex = int(self.sourceY.get())
			if yIndex < 0 or yIndex > 6:
				raise ValueError()
		except ValueError:
			messagebox.showwarning('Invalid Row', 'The row value must be an integer between 0 and 6.')
			return
		if xIndex in app.environment.state['sourceXIndices'] and yIndex in app.environment.state['sourceYIndices']:
			messagebox.showwarning('Source Already Exists', 'A source already exists in the provided location.')
			return
		self.sourceX.delete(0, tk.END)
		self.sourceY.delete(0, tk.END)
		app.environment.addSource(xIndex, yIndex)

	# Starts the simulation
	def runSimulation(self):
		self.runSimBtn.config(text='Pause Simulation', command=self.pauseSimulation)
		app.environment.run()

	# Pauses the simulation
	def pauseSimulation(self):
		self.runSimBtn.config(text='Run Simulation', command=self.runSimulation)
		app.environment.pause()

	# Resets all the values added to the environment
	def resetEnv(self):
		self.runSimBtn.config(text='Run Simulation', command=self.runSimulation)
		app.environment.resetState()


# Class to contain the content on the page that is not the displayed environment
class Content(tk.Frame):

	# Constructor
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.config(padx=30, bg='#150005')
		self.initWidgets()

	# Initialze the items to contain in the content
	def initWidgets(self):
		self.header = ContentHeader(self)
		self.header.grid(row=0, column=0)
		self.form = ContentForm(self)
		self.form.grid(row=1, column=0)


# Enviornment frame for viewing vehicles
class Environment(tk.Frame):

	# Constructor
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.width = 512
		self.height = 512
		self.running = False
		self.timeQuantum = 10
		self.sourceStrength = 2
		self.initCanvas()
		self.initState()

	# Initializes the environment state
	def initState(self):
		self.state = {
			'sourceXIndices': [],
			'sourceYIndices': [],
			'sources': [],
			'vehicle': Vehicle(self, self.canvas, self.width/2, self.height/2)
		}

	# Initializes the environment canvas
	def initCanvas(self):
		bgColor = '#333333'
		lineColor = '#476042'
		labelColor ='#FFFFFF'
		xSeg = self.width / 8
		ySeg = self.height / 8
		self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=bgColor)
		self.canvas.pack()
		# Creating grid
		for i in range(7):
			# Horizontal line
			self.canvas.create_line(0, xSeg*(i+1), self.width, xSeg*(i+1), fill=lineColor)
			self.canvas.create_text(10, xSeg*(i+1), text=str(i), fill=labelColor) # y label
			# Vertical line
			self.canvas.create_line(ySeg*(i+1), 0, ySeg*(i+1), self.height, fill=lineColor)
			self.canvas.create_text(ySeg*(i+1), 10, text=str(i), fill=labelColor) # x label

	# Adds a source to the current environment state
	def addSource(self, x, y):
		self.state['sourceXIndices'].append(x)
		self.state['sourceYIndices'].append(y)
		self.state['sources'].append(Source(self.canvas, (x+1)*(self.width/8), (y+1)*(self.height/8)))

	# Resets the state of the environment i.e. removes any sources and resets the vehicle
	def resetState(self):
		self.pause()
		for source in self.state['sources']:
			source.destroy()
		self.state['vehicle'].destroy()
		self.initState()

	# Gets the source value at the given canvas location
	def getSourceValue(self, x, y):
		distances = (np.array(self.state['sourceXIndices']) - x/(self.width/8)) ** 2 + (np.array(self.state['sourceYIndices']) - y/(self.width/8)) **2
		distances = np.sqrt(distances)
		strengths = self.sourceStrength / distances ** 2
		return np.sum(strengths)

	# Starts the environment simulation
	def run(self):
		self.running = True
		self.moveVehicle()

	# Continuously has the vehicle process the inputs at its current location while the simulation is running
	def moveVehicle(self):
		if (self.running):

			# Having the vehicle process the inputs at the given location
			rInput = self.getSourceValue(self.state['vehicle'].rSensor['x'], self.state['vehicle'].rSensor['y'])
			lInput = self.getSourceValue(self.state['vehicle'].lSensor['x'], self.state['vehicle'].lSensor['y'])
			self.state['vehicle'].processInput(rInput, lInput, self.timeQuantum)

			# Moving vehicle if it gets out of bounds
			if self.state['vehicle'].x < 0:
				self.state['vehicle'].moveTo(self.width + self.state['vehicle'].x, self.state['vehicle'].y)
			if self.state['vehicle'].x > self.width:
				self.state['vehicle'].moveTo(self.state['vehicle'].x - self.width, self.state['vehicle'].y)
			if self.state['vehicle'].y < 0:
				self.state['vehicle'].moveTo(self.state['vehicle'].x, self.height + self.state['vehicle'].y)
			if self.state['vehicle'].y > self.height:
				self.state['vehicle'].moveTo(self.state['vehicle'].x, self.state['vehicle'].y - self.height)

			# Calling to move the vehicle again
			self.canvas.after(self.timeQuantum, self.moveVehicle)

	# Pauses the environment simulation
	def pause(self):
		self.running = False


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


# Vehicle canvas object and controller
class Vehicle:

	# Contructor
	def __init__(self, parent, canvas, x, y):
		self.canvas = canvas
		self.environment = parent
		self.x = x
		self.y = y
		self.speedRatio = 0.5 # The conversion rate between the input sensor amount and the speed of the wheel
		self.width = 30
		self.height = 20
		self.maxSpeed = 1

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
			'y': self.y
		}
		self.rWheel = {
			'x': self.x - self.width/2,
			'y': self.y
		}

		# Rendering the vehicle drawing initially
		self.render()

	# Processes the given inputs for the two sensors of the vehicle, specifically, moving the 
	# vehicle for the given sensor inputs
	def processInput(self, rightInput, leftInput, duration):
		
		# Setting constant t to the duration of the movement
		t = duration

		# Getting the speed of each wheel, and their average speed
		vRight = self.speedRatio * rightInput if self.rSensor['attachment'] == 'right' else self.speedRatio * leftInput
		vRight = vRight if vRight < self.maxSpeed else self.maxSpeed
		if self.rSensor['inhibitory']:
			vRight = 1/vRight if vRight != 0 else self.maxSpeed
		vLeft = self.speedRatio * leftInput if self.lSensor['attachment'] == 'left' else self.speedRatio * rightInput
		vLeft = vLeft if vLeft < self.maxSpeed else self.maxSpeed
		if self.lSensor['inhibitory']:
			vLeft = 1/vLeft if vLeft != 0 else self.maxSpeed
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


# Main application object
class Application(tk.Tk):

	# Constructor
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title(APP_NAME)
		self.resizable(False, False)
		self.configure(padx=50, pady=50, background=BACKGROUND_COLOR)
		self.initWidgets()

	# Initialize the main widgets of the app
	def initWidgets(self):

		# Initialize the header info
		self.content = Content(self)
		self.content.grid(row=0, column=1)

		# Initialize the environment to display vehicles
		self.environment = Environment(self)
		self.environment.grid(row=0, column=0)


# MAIN -----------------------------------------------------------------------------------------------

# Main function
def main():
	global app
	app = Application()
	app.mainloop()

if __name__ == '__main__':
	main()

# Imports
import tkinter as tk
import numpy as np
from source import Source
from vehicle import Vehicle

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

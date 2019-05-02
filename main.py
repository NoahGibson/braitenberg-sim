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

# Import Tkinter for GUI handling
import tkinter as tk
from tkinter import messagebox

# Import the other classes
from environment import Environment

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

		# Initializing embedded frames
		addSourceFrame = tk.Frame(self, bg=self.parent['bg'])
		editLeftSensorFrame = tk.Frame(self, bg=self.parent['bg'])
		editRightSensorFrame = tk.Frame(self, bg=self.parent['bg'])
		simulationOptionsFrame = tk.Frame(self, bg=self.parent['bg'])

		# Add Source Frame
		# Add source label
		addSourceLabel = tk.Label(
			addSourceFrame,
			text='Add Source',
			font='Helvetica 14 bold',
			fg=TEXT_COLOR,
			bg=self.parent['bg'])
		addSourceLabel.grid(row=0, column=0, columnspan=5, sticky='w', pady=5)
		# Source X index label
		sourceXLabel = tk.Label(addSourceFrame, text='Column:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		sourceXLabel.grid(row=1, column=2, padx=5)
		# Source X index entry
		self.sourceX = tk.Entry(addSourceFrame, width=5, font=font, bg=entryBgColor, fg=entryFgColor, justify=tk.CENTER)
		self.sourceX.grid(row=1, column=3, padx=5)
		# Source Y index label
		sourceYLabel = tk.Label(addSourceFrame, text='Row:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		sourceYLabel.grid(row=1, column=0, padx=5)
		# Source Y index entry
		self.sourceY = tk.Entry(addSourceFrame, width=5, font=font, bg=entryBgColor, fg=entryFgColor, justify=tk.CENTER)
		self.sourceY.grid(row=1, column=1, padx=5)
		# Add Source confirm
		sourceConfirm = tk.Button(addSourceFrame, text='Add Source', width=20, font='Helvetica 10 bold', command=self.addSource)
		sourceConfirm.grid(row=1, column=4, padx=20)

		# Edit Left Sensor
		# Edit left Sensor label
		editLeftSensorLabel = tk.Label(
			editLeftSensorFrame,
			text='Edit Left Sensor',
			font='Helvetica 14 bold',
			fg=TEXT_COLOR,
			bg=self.parent['bg'])
		editLeftSensorLabel.grid(row=0, column=0, columnspan=5, sticky='w', pady=(10, 5))
		# Left sensor attachment Label
		lSAttachLabel = tk.Label(editLeftSensorFrame, text='Output Wheel:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		lSAttachLabel.grid(row=1, column=0, padx=5)
		# Left sensor attachment
		self.lSAttach = tk.StringVar(value='left')
		lSAttachLeft = tk.Radiobutton(editLeftSensorFrame, variable=self.lSAttach, value='left', text='Left', width=7, font='Helvetica 10 bold', indicatoron=0)
		lSAttachLeft.grid(row=1, column=1, padx=5)
		lSAttachRight = tk.Radiobutton(editLeftSensorFrame, variable=self.lSAttach, value='right', text='Right', width=7, font='Helvetica 10 bold', indicatoron=0)
		lSAttachRight.grid(row=1, column=2, padx=5)
		# Left sensor inhibit label
		lSInhibitLabel = tk.Label(editLeftSensorFrame, text='Inverse:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		lSInhibitLabel.grid(row=1, column=3, padx=5)
		# Left sensor inhibit
		self.lSInhibit = tk.BooleanVar(value=False)
		lSInhibitPick = tk.Checkbutton(editLeftSensorFrame, variable=self.lSInhibit, text='Inverse', width=7, font='Helvetica 10 bold', indicatoron=0)
		lSInhibitPick.grid(row=1, column=4, padx=5)

		# Edit right Sensor
		# Edit right Sensor label
		editRightSensorLabel = tk.Label(
			editRightSensorFrame,
			text='Edit Right Sensor',
			font='Helvetica 14 bold',
			fg=TEXT_COLOR,
			bg=self.parent['bg'])
		editRightSensorLabel.grid(row=0, column=0, columnspan=5, sticky='w', pady=(10, 5))
		# Right sensor attachment Label
		rSAttachLabel = tk.Label(editRightSensorFrame, text='Output Wheel:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		rSAttachLabel.grid(row=1, column=0, padx=5)
		# Right sensor attachment
		self.rSAttach = tk.StringVar(value='right')
		rSAttachLeft = tk.Radiobutton(editRightSensorFrame, variable=self.rSAttach, value='left', text='Left', width=7, font='Helvetica 10 bold', indicatoron=0)
		rSAttachLeft.grid(row=1, column=1, padx=5)
		rSAttachRight = tk.Radiobutton(editRightSensorFrame, variable=self.rSAttach, value='right', text='Right', width=7, font='Helvetica 10 bold', indicatoron=0)
		rSAttachRight.grid(row=1, column=2, padx=5)
		# Right sensor inhibit label
		rSInhibitLabel = tk.Label(editRightSensorFrame, text='Inverse:', font=font, fg=TEXT_COLOR, bg=self.parent['bg'])
		rSInhibitLabel.grid(row=1, column=3, padx=5)
		# Right sensor inhibit
		self.rSInhibit = tk.BooleanVar(value=False)
		rSInhibitPick = tk.Checkbutton(editRightSensorFrame, variable=self.rSInhibit, text='Inverse', width=7, font='Helvetica 10 bold', indicatoron=0)
		rSInhibitPick.grid(row=1, column=4, padx=5)

		# Simulation options frame
		# Run the simulation
		self.runSimBtn = tk.Button(simulationOptionsFrame, text='Run Simulation', font='Helvetica 14 bold', width=30, command=self.runSimulation)
		self.runSimBtn.grid(row=0, column=0, columnspan=5, pady=(30, 10))
		# Reset the sources and vehicle
		self.resetBtn = tk.Button(simulationOptionsFrame, text='Reset', font='Helvetica 10 bold', width=7, command=self.resetEnv)
		self.resetBtn.grid(row=1, column=0, columnspan=5, pady=(10, 20))

		# Packing the frames
		addSourceFrame.pack(fill=tk.X)
		editLeftSensorFrame.pack(fill=tk.X)
		editRightSensorFrame.pack(fill=tk.X)
		simulationOptionsFrame.pack(anchor='center')

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

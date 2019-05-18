# Braitenberg Vehicle Simulator

Braitenberg Vehicles are autonomous agents consisting of simple sensors and actuators. In most examples, the sensors detect light, and the actuators are wheel motors. When connected and configured in various ways, these basic hardware components can lead to the vehicle appearing to exhibit various goal oriented behaviors such as "avoiding" sources or "attacking" them.

This Python-based simulator allows for the editing of basic configurations for a Braitenberg vehicle, as well as a view of its behavior in an environment of sources.

![Simulation Preview](preview.PNG)


## Manual

<dl>
  <dt>Add Source</dt>
  <dd>Adds a new source at the given row and column in the vehicle environment. A source produces an output field of values that decrease with the square of the distance from the source. These values are what the vehicle sensors detect.</dd>
  <dt>Edit Sensor Output Wheel</dt>
  <dd>The wheel to which that sensor's output is directed to. The sensor output is what affects the speed of the wheel. If no sensor's output is sent to a wheel, then that wheel will remain stationary.</dd>
  <dt>Edit Sensor Inverse</dt>
  <dd>Whether or not the sensor's output value should be inversed, that is, it will send a low value if it senses a high value, and vice versa.</dd>
  <dt>Edit Wheel Inverse</dt>
  <dd>Whether or not the velocity of the wheel should be inversed, that is, it will have a low speed if it receives a high sensor input value, and vice versa.</dd>
</dl>


## Setting up Development Environment

*Note: Make sure you have both Python 3 and virtualenv installed on your machine*

1. Open a command window within the project directory and run the command ```new_env```. This will create a new virtual environment and install all the necessary Python packages.
2. Run the command ```Scripts\activate.bat```. This will activate the virtual environment so any changes in Python packages will only be made locally for the project.
3. Run ```python main.py``` in order to launch the simulator interface.
4. When finished wtih any edits, run ```deactivate``` to close the virtual environment.


## Generating Executable File

The simulator can be packaged into a standalone Windows executable file. To do this run the command:

```pyinstaller --noconsole --onefile --name braitenberg --add-data favicon.ico;. --icon="favicon.ico" main.py```

# Self_Driving_Car-CT213_2023

## Name
Self-driving car simulation

## Description
This project aims to use neural networks to train simulated car to avoid obstacles by two different methods: Imitation Learning and Genetic Algorithm.

## Installation
Adiciona aí Omisso, namoral

Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage

### Adjusting simulation parameters

It is possible to adjust the parameters of the simulation, as in the car width, maximum velocity, number of sensors, etc. To do this, simply go to the file "simulation_constants.py" and change the values to better fit the situation you desire.

### Training a neural network using Imitation Learning

To train the neural network, first you need to run the code in "main_playable.py" to generate a dataset containing the input and expected output. After running it, the simulation will start and you will be able to control the car with the arrow keys or WASD.
For better results, try to control the car using the same logic for when to do a specific action, such as only changing lanes when a sensor detects another car in the lane you currently are in, rather than doing it as soon as you see it.
If you want a larger dataset, you can change the number of vehicles that appear, go to the file "simulation.py" and in line 34 change the number in the definition of "self.dummies".

To create and train the neural network you created, as well as to test if it is able to properly function, run the code in "main_simulation.py" with the integer "option" set as 2 and with the boolean "Train_new_model" set as True. The resulting neural network will be saved in a H5 file with the name chosen in line 40.
You can change how the neural network is defined, as well as the number of epochs and the batch size for training, in the function "get_model", which is defined in "Car.py".

If you are not satisfied with the results obtained, it is possible to make corrections in the neural network by creating a smaller dataset while running the code in "main_simulation.py" with the integer "option" set as 2 and with the boolean "Train_new_model" set as False. To do this, use the arrow keys or WASD when a wrong decision is made. After you have closed the simulation, the neural network will be trained again and saved in a H5 file.
For better results, when generating a new dataset for training only press a few times the correct key when the car makes a mistake.

A H5 file containing a functioning neural network trained using Imitation Learning can be loaded in "main_simulation.py" is available in the repository as "Imitation.h5".

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

# Playing Snake Using Artificial Intelligence and Neural_Network

## Introduction
Hiii, i created a <b> a self learning artificial intelligence </b> </br>
The main methods are:</br></br>
<strong>
1.Artificial Neural Network (Using Weights and Biases to control snake's movement</br>
2.Genetic Algorithm (To update weights and biases)</strong>

## How Does It Works?????
I design snake to look in 8 direction (North, East, South, West, NorthEast, SouthEast, SouthWest, NorthWest) Respectively. See Picture Below </br>
The vector in 8 direction is looking for: </br>
1. Distance to wall </br>
2. Distance to food </br>
3. Distance to its body </br>

![Snake Direction](https://user-images.githubusercontent.com/59665617/99031549-ec5ab380-25a9-11eb-9603-25072cf88adf.png)

Therefore there will be 24 input neurons (8 distance to wall, 8 distance to food, 8 distance to its body Then input value will go forward into neuron in next hidden layer neuron. After all input, weights and biases are being feedforwarded. The final result will be calculated into 4 output and decides whether snake will go UP, RIGHT, LEFT, or DOWN based on final calculation.</br>

<strong> The activation function used in feedforward is sigmoid function </strong>

![Neuron](https://user-images.githubusercontent.com/59665617/99032150-5d4e9b00-25ab-11eb-8fe5-33353e3395e5.png)

## DEMO

<strong> Arena.py </strong> control arena display, neural network display </br>
<strong> Food.py </strong> control food intialization, food position, drawing food </br>
<strong> Snake.py </strong> control snake movement, snake display, and gameover check </br>
<strong> NeuralNetwork.py </strong> control all about neural network, architecture, bias production, weight production</br>
<strong> Vector.py </strong> control snake visions in 8 direction</br>
<strong> Parameters.py </strong> contain all parameter value such as neural network shape, grid size, arena color, population number</br>
<strong> Training/Genetic_Snake..py </strong> control genetic algorithm process

![ezgif com-gif-maker](https://user-images.githubusercontent.com/59665617/99032999-12ce1e00-25ad-11eb-98df-b8801a497248.gif)


## ACKNOWLEDGEMENT

I am inspired by a youtuber named code bullet for the method to play snakes

Code Bullet Youtubbe Link: https://www.youtube.com/results?search_query=code+bullet
My Youtube Link: https://youtu.be/sQCklZbfF48

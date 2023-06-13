# PPY_PROJECT
Final project for PPY

This is a small 2d game made in Python, using pygame module.
In this game you controll a spaceship, which can move by A and D keys to the left or right respectively
The game is infinite, however a player can lose by colliding with some of the meteors
To destroy a meteor and increase the score, player must solve a simple equation, which is shown on the screen, and collide with the meteor that has a correct answer written on it.

Classes:
ParticleSystem - this class is used to simulate basic particle effects. It has 3 methods: emit(), add_particles() and destroy_particles(); add_particles method is used to create a specific amount of particles providing with size, direction of moving and starting position. In emit() method, particles are moving and shrinking, 
in destroy_particles() method, system checks for particles current size and if its less or equal to 0 - remove them from the list.

EquationManager - this class stands for the creating an equation which is used in main game loop. It creates an equation and generates 2 random "answers" and one true answer for it.

Score class stands for calculating players current score, saving highscore to the generated file(only if current score higher than highscore) and loading data from a file.

Colors class is used to store all usefull colors as enum, to make it easier to use them in main game loop.

In game_object_manager file, 3 classes can be found: GameObject, Player and Meteor. Each of them are representing "actors" of the system. Player and Meteor classes are inherit from GameObject class and has some unique attributes such as equation and answer. In Player class, system stores current equation and correct answer to make it easier to render equation in a text form and check if player has solved the equation correctly by comparing the answer on meteor and the correct one.

The core game loop happens in main file. There are few methods, which are stand for rendering game window and all graphics, executing main game logic, collision detection and input detection.

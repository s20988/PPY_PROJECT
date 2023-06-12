import pygame

class GameObject:

    def __init__(self, image, sizeX, sizeY, posX, posY):
        self.sprite = pygame.image.load(image)
        self._transform = pygame.transform.scale(self.sprite, (sizeX, sizeY))
        self._position = pygame.Rect(posX - sizeX / 2, posY + sizeY * 2, self._transform.get_width(), self._transform.get_height())
    
    @property
    def position(self):
        return self._position
    
    @property
    def transform(self):
        return (self._transform.get_width(), self._transform.get_height())

class Player(GameObject):
    
    def __init__(self, image, sizeX, sizeY, posX, posY, velocity, answer, equation):
        super().__init__(image, sizeX, sizeY, posX, posY)
        self._velocity = velocity
        self._answer = answer
        self._equation = equation
        self._health = 3
    
    @property
    def velocity(self):
        return self._velocity
    
    def take_damage(self, damage):
        self._health -= damage
        if self._health <= 0:
            self._position.y = 10000

    
    @property
    def answer(self):
        return self._answer
    
    def set_answer(self, answer):
        self._answer = answer

    @property
    def equation(self):
        return self._equation

    def set_equation(self, equation):
        self._equation = equation

        

class Meteor(GameObject):
    _answer:int
    _velocity:int
    def __init__(self, image, sizeX, sizeY, posX, posY, answer):
        super().__init__(image, sizeX, sizeY, posX, posY)
        self._velocity = 2
        self._answer = answer

    def check_collision(self, rect:pygame.Rect):
        return self._position.colliderect(rect)

    @property
    def answer(self):
        return self._answer

    @property
    def velocity(self):
        return self._velocity

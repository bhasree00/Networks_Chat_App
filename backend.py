import pygame

class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 1
    
    def display(self):
        pygame.draw.circle(screen, self.color, self.x, self.y, self.size, self.thickness)

background_colour = (0, 105, 148)
(width, height) = (500, 700)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Battleship')
screen.fill(background_colour)
pygame.display.flip()

particleOne = Particle(100, 100, 30)
particleOne.display()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # QUIT code is 256
            running = False
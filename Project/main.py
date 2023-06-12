import pygame
import colors
import os
import game_object_manager
import game_manager
import random

pygame.font.init()

WIDTH, HEIGHT = 512, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")

BACKGROUND_COLOR = colors.Colors.DARK_BLUE
CHARACTER_SPACE_SHIP_IMAGE = os.path.join('Assets', 'spaceship.png')
METEOR_IMAGES = []
for m in range(3):
    METEOR_IMAGES.append(os.path.join("Assets\Meteors", f"meteor{m}.png"))

EQUATION = game_manager.EquationManager()
ANSWERS = EQUATION.generate_random_equation()
SCORE = game_manager.Score()
PLAYER = game_object_manager.Player(CHARACTER_SPACE_SHIP_IMAGE, 64, 64, WIDTH / 2, HEIGHT / 2, 5, EQUATION.answer, EQUATION.equation)

METEORS = []

FPS = 60
text_font = pygame.font.SysFont("comicsans", 20)

class ParticleSystem:
    def __init__(self, life_time):
        self.particles = []
        self._life_time = life_time
    
    @property
    def life_time(self):
        return self._life_time
    
    def emit(self, color, noiseX:list, noiseY:list):
        if self.particles:
            self.destroy_particles()
            for particle in self.particles:
                particle[0][0] += particle[2][0] * random.choice(noiseX)
                particle[0][1] += particle[2][1] * random.choice(noiseY)
                particle[1] -= 0.2
                pygame.draw.circle(WINDOW, color, particle[0], int(particle[1])) 

    def add_particles(self, posX, posY, dirX, dirY):
        pos_x = posX
        pos_y = posY
        radius = random.randint(5, 10)
        direction_x = dirX
        direction_y = dirY
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def destroy_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


PARTICLE_EVENT = pygame.USEREVENT + 1
PARTICLE_SYSTEM = ParticleSystem(FPS)
EXPLOSION_PARTICLES = ParticleSystem(FPS*2)
METEOR_EXPLOSION_PARTICLES = ParticleSystem(FPS*2)

def spawn_meteors():
    EQUATION = game_manager.EquationManager()
    ANSWERS = EQUATION.generate_random_equation()
    METEORS.clear()
    PLAYER.set_equation(EQUATION.equation)
    PLAYER.set_answer(EQUATION.answer)
    random.shuffle(ANSWERS)
    for m in range(3):
        METEORS.append(game_object_manager.Meteor(random.choice(METEOR_IMAGES), 64, 64, 64 + WIDTH / 3 * m, -HEIGHT/4, ANSWERS[m]))

def handle_inputs():
    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_a] and PLAYER.position.x - PLAYER.velocity > 0:
        PLAYER.position.x -= PLAYER.velocity
    if key_input[pygame.K_d] and PLAYER.position.x + PLAYER.velocity < WIDTH - PLAYER.transform[0]:
        PLAYER.position.x += PLAYER.velocity
    if key_input[pygame.K_ESCAPE]:
        SCORE.save_score()
        pygame.quit()

def handle_meteors():
    for x in range(len(METEORS)):
        METEORS[x].position.y += METEORS[x].velocity
        if METEORS[x].position.y + METEORS[x].velocity > HEIGHT:
            spawn_meteors()
                 

def draw_window():
    WINDOW.fill(BACKGROUND_COLOR.value)
    WINDOW.blit(PLAYER._transform, PLAYER.position)
    for x in range(len(METEORS)):
        WINDOW.blit(METEORS[x]._transform, METEORS[x].position)
        answer_txt = str(METEORS[x].answer)
        answer = text_font.render(answer_txt, 1, colors.Colors.WHITE.value)
        WINDOW.blit(answer, (METEORS[x].position.x, METEORS[x].position.y - answer.get_height()/2))
    equation = text_font.render(PLAYER.equation, 1, colors.Colors.WHITE.value)
    WINDOW.blit(equation, (PLAYER.position.x, PLAYER.position.y - equation.get_height()/2))
    PARTICLE_SYSTEM.emit(colors.Colors.YELLOW.value, [-0.2, 0.2], [1, 1])
    EXPLOSION_PARTICLES.emit(colors.Colors.ORANGE.value, [-1, 1], [-1, 1])
    METEOR_EXPLOSION_PARTICLES.emit(colors.Colors.DARK_GREY.value, [-1, 1], [-1, 1])
    score_text = text_font.render(f"SCORE: {SCORE.score}", 1, colors.Colors.WHITE.value)
    highscore_text = text_font.render(f"HIGHSCORE: {SCORE.highscore}", 1, colors.Colors.AQUA.value)
    WINDOW.blit(score_text, (WIDTH/2 - 50, 0))
    WINDOW.blit(highscore_text, (WIDTH/2 - 50, 50))
    pygame.display.update()

def check_collisions():
    for i in range(len(METEORS)):
        if METEORS[i].check_collision(PLAYER._position):
            if METEORS[i].answer == PLAYER.answer:
                clone_meteors = METEORS
                clone_meteors.remove(METEORS[i])
                SCORE.add_score(1)
                for j in range(20):
                    METEOR_EXPLOSION_PARTICLES.add_particles(PLAYER.position.x + random.randint(-10, 10), 
                                                      PLAYER.position.y + random.randint(-10, 10),
                                                      random.randint(-10, 10), random.randint(-10, 10))
                return
            for i in range(20):
                EXPLOSION_PARTICLES.add_particles(PLAYER.position.x + random.randint(-10, 10), 
                                                      PLAYER.position.y + random.randint(-10, 10),
                                                      random.randint(-10, 10), random.randint(-10, 10))
            PLAYER.take_damage(1)
            SCORE.save_score()
 

def main():
    clock = pygame.time.Clock()
    pygame.time.set_timer(PARTICLE_EVENT, PARTICLE_SYSTEM.life_time)
    is_run = True
    while is_run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
                return
            if event.type == PARTICLE_EVENT:
                PARTICLE_SYSTEM.add_particles(PLAYER.position.x + PLAYER.transform[0]/2, 
                                              PLAYER.position.y + PLAYER.transform[1]/2, 
                                              PLAYER.velocity, PLAYER.velocity)
        
        if(len(METEORS) == 0):
            spawn_meteors()
        handle_meteors()
        handle_inputs()
        check_collisions()
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
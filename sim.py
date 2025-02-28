import pygame 
import time
import math

pygame.init()

#Window Setup
screen_width = 800
screen_height = 600


background_color = (200, 200, 200)  # White color
rect_color = (125, 0, 0)
target_color = (10,10,10)

screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.SCALED, vsync=1)

rect_width = 100
rect_length = 100

#Global Constants
goal_x = screen_width/2
friction_force = 0.1

#utils
def sign(num):
    if num < 0:
        return -1
    else:
        return 1

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

class Rect:
    def __init__(self, n_color, n_kp, n_y_rect):
        self.color = n_color
        self.kp = n_kp
        #PID Variables
        self.error_p = 0

        #Rect Properties
        self.m_rect = 1.0
        self.a_rect = 0.0
        self.v_rect = 0.0

        self.x_rect = 0.0
        self.y_rect = screen_height/2.0 + n_y_rect

        self.width_rect = 100
        self.length_rect = 100

    def update_rect(self):
        self.error_p = goal_x - self.x_rect
        self.v_rect += self.error_p * self.kp
        self.v_rect -= friction_force * self.v_rect
        self.x_rect += self.v_rect

        if abs(self.error_p) < 0.01: #Nice smoothing
            self.x_rect = goal_x
    
    def draw_rect(self, screen):
        pygame.draw.rect(screen, self.color, (self.x_rect, self.y_rect, self.width_rect, self.length_rect), border_radius=5)

running = True
rect_list = [Rect((125,0,0), 0.006, 100), Rect((0,125,0), 0.0037, -50), Rect((0,0,125), 0.0025, -200)]

while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        goal_x -= 10
    if keys[pygame.K_RIGHT]:
        goal_x += 10
    goal_x = clamp(goal_x, 0, screen_width - 100)
    

    screen.fill(background_color)
    pygame.draw.rect(screen, target_color, (goal_x, 0, screen_width, screen_height))
    for rect in rect_list:
        rect.update_rect()
        rect.draw_rect(screen)
    pygame.display.update()
    time.sleep(0.005)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()

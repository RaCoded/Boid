import pygame
import random
from boid import Boid  # Assure-toi que ta classe Boid est dans un fichier nommé boid.py


# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
BOID_COLOR = (255, 255, 255)
NUM_BOIDS = 50

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Boids")

# Création d'une liste de boids
boids = [Boid(random.randint(0.0, WIDTH), random.randint(0.0, HEIGHT)) for _ in range(NUM_BOIDS)]

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour des boids
    for boid in boids:
        boid.adaptation()
        boid.collision(WIDTH, HEIGHT)

    # Dessin
    screen.fill(BACKGROUND_COLOR)
    for boid in boids:
        pygame.draw.circle(screen, BOID_COLOR, (int(boid.position[0]), int(boid.position[1])), 5)

    pygame.display.flip()
    clock.tick(60)  # Limite à 60 images par seconde

pygame.quit()
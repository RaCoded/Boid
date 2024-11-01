import pygame
import random
from boid import Boid  
import math
import cv2
import numpy as np


def draw_boid(screen, color, position, velocity):
    """Dessine un boid en forme de triangle"""
    # Taille du boid
    boid_size = 10
    # Points du triangle
    points = [
        (0, -boid_size),    # Point supérieur (sommet)
        (boid_size, boid_size),  # Point inférieur droit
        (-boid_size, boid_size)  # Point inférieur gauche
    ]
    
    # Calculer l'angle de rotation en radians
    angle = math.atan2(velocity[1], velocity[0])  # Angle en radians
    # Appliquer la rotation
    rotated_points = []
    for x, y in points:
        # Rotation de la forme
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        rotated_points.append((rotated_x + position[0], rotated_y + position[1]))
    # Dessin du boid
    pygame.draw.polygon(screen, color, rotated_points)


# Configuration de la fenêtre et des boids
width, height =  1000, 1000
couleur_fond=(10,0,0)
couleur_boid=(0,100,0)
nombre_boids=50


# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Boids")

# Création d'une liste de boids
boids = [Boid(random.uniform(0, width), random.uniform(0, height)) for _ in range(nombre_boids)]

# Boucle principale
running = True
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour des boids
    for boid in boids:
        #Calcul du comportement
        boid.comportement(boids)
        #Calcul de l'adaptation
        boid.adaptation()
        #Calcul des collisions
        boid.collision(width, height)

    # Dessin
    screen.fill(couleur_fond)
    for boid in boids:
        # Dessiner le boid en forme de flèche
        draw_boid(screen, couleur_boid, (int(boid.position[0]), int(boid.position[1])), boid.vitesse)

    #Double bufferring (pas de problèmes graphique)
    pygame.display.flip()
    #On limite à 60 fps
    clock.tick(60)  

pygame.quit()

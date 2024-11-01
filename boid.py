import random
import numpy as np


class Boid:
#Constructeur du boid
    def __init__(self,x,y):
        #Position, vitesse acceleration
        self.position= np.array([x,y],dtype=float)
        self.vitesse=np.array([random.uniform(-1,1),random.uniform(-1,1)], dtype=float)
        self.acceleration = np.array([0.0, 0.0], dtype=float)
        #Bornes max de la vitesse et des forces appliquées au boid
        self.vitesse_max=10.0
        self.force_max=1.0
        self.perception_radius=75.0

        self.alignement_fact=0.7
        self.cohesion_fact=0.5
        self.separation_fact=10

#appliquer une force au boid = modifier son accélération
    def appliquer_force(self,force):
        force = np.array(force, dtype=float)
        self.acceleration+=force

#adapter la vitesse et la position du Boid
    def adaptation(self):
        self.acceleration=np.clip(self.acceleration, -self.force_max, self.force_max)
        #Mise à jour de la vitesse en fonction de l'accélération
        self.vitesse+=self.acceleration
        #Limitation de la vitesse sur l'abscisse et l'orodonée.
        if abs(self.vitesse[0])>self.vitesse_max:
            self.vitesse[0] = self.vitesse_max * np.sign(self.vitesse[0])
        if abs(self.vitesse[1])>self.vitesse_max:
            self.vitesse[1] = self.vitesse_max * np.sign(self.vitesse[1])
        #remise à 0 de l'accélération. Choix temporaire.
        self.acceleration=np.array([0.0, 0.0], dtype=float)
        #mise à jour de la position
        self.position+=self.vitesse

        

#Gestion des collisions aux bords
    def collision(self,width,height):
        if self.position[0] > width :
            self.position[0] = 0
        elif  self.position[0] < 0:
            self.position[0]=width 
        if self.position[1] > height:
            self.position[1] = 0
        elif  self.position[1] < 0:
            self.position[1]=height 
           
#Comportement du Boid en présence de voisins dans son radius 
    def comportement(self, boids):
        # Les 3 grandes forces
        alignement = np.array([0.0, 0.0], dtype=float)
        cohesion = np.array([0.0, 0.0], dtype=float)
        separation = np.array([0.0, 0.0], dtype=float)

        # Propriétés relatives au Boid
        nb_voisins = 0
        distance_separation = 40

        # Algo comportemental
        for other_boid in boids:
            distance_to_other = np.linalg.norm(self.position - other_boid.position)
            if other_boid != self and distance_to_other < self.perception_radius:
                alignement += other_boid.vitesse
                cohesion += other_boid.position
                if distance_to_other < distance_separation:
                    separation += (self.position - other_boid.position)/(distance_to_other+0.001)
                nb_voisins += 1
                
        if nb_voisins > 0:
            # Alignement
            alignement /= nb_voisins
            if np.linalg.norm(alignement) > 0:  # Vérification pour éviter NaN
                alignement = alignement / np.linalg.norm(alignement) * self.vitesse_max
            else:
                alignement = np.array([0.0, 0.0], dtype=float)
            alignement_force = alignement - self.vitesse

            # Cohesion
            cohesion /= nb_voisins
            cohesion -= self.position
            if np.linalg.norm(cohesion) > 0:  # Vérification pour éviter NaN
                cohesion = cohesion / np.linalg.norm(cohesion) * self.vitesse_max
            else:
                cohesion = np.array([0.0, 0.0], dtype=float)
            cohesion_force = cohesion - self.vitesse

            # Separation
            if np.linalg.norm(separation) > 0:  # Vérification pour éviter NaN
                separation = separation / np.linalg.norm(separation) * self.force_max
            separation_force = separation

            # Appliquer les forces
            self.appliquer_force(alignement_force * self.alignement_fact)
            self.appliquer_force(cohesion_force * self.cohesion_fact)
            self.appliquer_force(separation_force * self.separation_fact)

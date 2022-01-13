#importation des modules neccéssaires 
import pygame
pygame.init()
import sys
import math
import random


#Crétation de la fenêtre et de l'horloge
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

#Instanciation de la classe joueur
class Player:
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.etat = "vivant"

    def main(self, display) : #Fonction qui va s'occuper de toutes les actions du joueur
        pygame.draw.rect(display, (0, 0, 255), (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for balle in balles_ennemis :
            if self.rect.colliderect(balle.rect) :
                self.etat = "mort"


#Instaciation de la classe Balle
class Balle_Joueur:
    def __init__ (self, x, y ,mouse_x, mouse_y) :
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        #Calcul des angles pour le tir de la balle
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed


    def main(self, display) : #Fonction qui s'occupe des action de la balle
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        self.rect = pygame.Rect(self.x, self.y, 5, 5)

#Instanciation de la classe Ennemi
class Ennemi:
    def __init__ (self, x, y, width, height) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def main(self, display) :
        self.angle = math.atan2(self.y-player.y, self.x-player.x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.rect.colliderect(player.rect) :
            player.etat = "mort"

#Instaciation de la classe Tireur_Ennemi
class Tireur_Ennemi:
    def __init__ (self, x, y, width, height) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.tick = 0
        self.but_x = random.randint (0, 800)
        self.but_y = random.randint (0, 600)

    def main(self, display) :
        self.tick += 1
        pygame.draw.rect(display, (255, 255, 0), (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.tick < 120 :
            self.angle = math.atan2(self.y-self.but_y, self.x-self.but_y)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
            self.x -= int(self.x_vel)
            self.y -= int(self.y_vel)
        if self.tick == 180 :
            balles_ennemis.append(Balle_Ennemi(self.x, self.y))
            self.tick = 0
            self.but_x = random.randint (0, 800)
            self.but_y = random.randint (0, 600)

#Instaciation de la classe Balle

class Balle_Ennemi:
    def __init__ (self, x, y) :
        self.x = x
        self.y = y
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        #Calcul des angles pour le tir de la balle
        self.angle = math.atan2(y-player.y, x-player.x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display) : #Fonction qui s'occupe des action de la balle
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        self.rect = pygame.Rect(self.x, self.y, 5, 5)

#Instanciation de la classe DASH

class Dash:
    def __init__ (self, x, y, width, height) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 15
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.tick = 0
        self.angle = math.atan2(y-player.y, x-player.x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    
    def main(self, display) :
        self.tick += 1
        if self.tick == 180 :
            self.angle = math.atan2(self.y-player.y, self.x-player.x)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
        if (self.tick < 240) and (self.tick > 180) :
            self.x -= int(self.x_vel)
            self.y -= int(self.y_vel)
        if self.tick == 240 :
            self.tick = 0
        if self.rect.colliderect(player.rect) :
            player.etat = "mort"
        pygame.draw.rect(display, (255, 128, 0), (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

player= Player(400, 300, 32, 32) #Création du jeu

pos_x = list(range(20, player.x - 100)) + list(range(player.x + 100, 780))
pos_y = list(range(20, player.y - 100)) + list(range(player.y + 100, 580))

positions_objets= [0, 0] #Première valeur = x, deuxième = y. Permet le déplacement de tous les objets autour du joueur

balles_joueur = [] #Permet de gérer l'action de toutes les balles en les ajoutant dans la liste
balles_ennemis = []
ennemis = [] #Permet de gérer l'action de tous les ennemis en les ajoutant à la liste
score = 0
tick = 0
vague = 1

myfont = pygame.font.SysFont("monospace", 30)
score_display = myfont.render(str(score), 1, (255,255,0))
display.blit(score_display, (0, 0))
meilleur_score_display =  0




#ennemis.append(Tireur_Ennemi(random.randint(20, 780), random.randint(20, 580), 20, 20))
t_ennemi = random.randint(1, 10)
t_ennemi = random.randint(1, 10)
if t_ennemi <7 :
    ennemis.append(Ennemi(random.choice(pos_x), random.choice(pos_y), 20, 20))
elif t_ennemi < 9 :
    ennemis.append(Tireur_Ennemi(random.choice(pos_x), random.choice(pos_y), 20, 20))
else :
    ennemis.append(Dash(random.choice(pos_x), random.choice(pos_y), 20, 20))

#Boucle de jeu infinie
while True:
    display.fill((133, 109, 77)) #remplissage du fond
    score_display = myfont.render(str(score), 1, (255,255,0))
    display.blit(score_display, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos() 
    
    #Spawn ennmis toutes les 5 secondes
    tick += 1
    if tick == 300 :
        tick = 0
        for i in range (vague) :
            t_ennemi = random.randint(1, 10)
            if t_ennemi <7 :
                ennemis.append(Ennemi(random.choice(pos_x), random.choice(pos_y), 20, 20))
            elif t_ennemi < 9 :
                ennemis.append(Tireur_Ennemi(random.choice(pos_x), random.choice(pos_y), 20, 20))
            else :
                ennemis.append(Dash(random.choice(pos_x), random.choice(pos_y), 20, 20))
        vague += 1
    

    for event in pygame.event.get(): #Récupération des evenements
        if event.type == pygame.QUIT : #Permet de quitter proprement pygame
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN : #Permet de savoir si un bouton de la souris a été pressé
            if event.button == 1:
                balles_joueur.append(Balle_Joueur(player.x, player.y, mouse_x, mouse_y )) #Crée une balle et l'ajoute dans la liste des balles
    keys = pygame.key.get_pressed() #Récupère toutes les touches qui ont été pressées

    pygame.draw.rect(display, (255, 255, 255), (100-positions_objets[0], 100-positions_objets[1], 16, 16))

    #Permet le déplacement en affectant la position de tous les objets exepté le joueur en jouant sur les valeur
    if keys[pygame.K_q]:
        positions_objets[0] -= 5

        for balle in balles_joueur :
            balle.x += 5
        for balle in balles_ennemis :
            balle.x += 5
        for ennemi in ennemis :
            ennemi.x += 5
    if keys[pygame.K_d]:
        positions_objets[0] += 5

        for balle in balles_joueur :
            balle.x -= 5
        for balle in balles_ennemis :
            balle.x -= 5
        for ennemi in ennemis :
            ennemi.x -= 5

    if keys[pygame.K_z]:
        positions_objets[1] -= 5
        
        for balle in balles_joueur :
            balle.y += 5
        for balle in balles_ennemis :
            balle.y += 5
        for ennemi in ennemis :
            ennemi.y += 5

    if keys[pygame.K_s]:
        positions_objets[1] += 5

        for balle in balles_joueur :
            balle.y -= 5
        for balle in balles_ennemis :
            balle.y -= 5
        for ennemi in ennemis :
            ennemi.y -= 5

    player.main(display) #Appel de la fonction main qui permet l'action du joueur 
    for balle in balles_joueur: #Appel de la fonction main de toutes les balles
        balle.main(display)
    for ennemi in ennemis: #Appel de la fonction main de tous les ennemis
        ennemi.main(display)
    for balle in balles_ennemis :
        balle.main(display)

    for balle in balles_joueur :
        for ennemi in ennemis:
            if balle.rect.colliderect(ennemi.rect) :
                ennemis.remove(ennemi)
                score += 1
    
    file = open("meilleurs_scores.txt", "r+")
    best_score = int(file.readline())
    
    # Si le score du joueur est meilleur que le meilleur score on actualise le meilleur score
    if score > best_score:
        file = open("meilleurs_scores.txt", "w")
        file.write(str(score))
        file.close()

    meilleur_score_display = myfont.render(str(best_score), 1, (255,255,255))
    display.blit(meilleur_score_display, (0, 30))


    if player.etat == "mort" : 
        while True :
            for event in pygame.event.get(): #Récupération des evenements
                if event.type == pygame.QUIT : #Permet de quitter proprement pygame
                    sys.exit()
            
    clock.tick(60) #Permet de faire tourner le jeu à 60 fps
    pygame.display.update() #Update la fenêtre

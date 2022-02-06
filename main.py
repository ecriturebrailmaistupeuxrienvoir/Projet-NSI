#importation des modules neccéssaires 
import pygame
pygame.init()
import sys
import math
import random
import bdd_main

import sqlite3




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
        self.animation = 0
        self.image = images_balles[self.animation]
        self.rect = self.image.get_rect()
        self.arme = "repos"
        self.etat = "vivant"
        self.tick = 0

    def animation_joueur(self, display) :
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180/math.pi) * -math.atan2(rel_y, rel_x)

        self.image = pygame.transform.rotate(images_joueur[self.animation], angle)
         
        self.rect.x = self.x
        self.rect.y = self.y
        display.blit(self.image, self.rect)

    def main(self, display) : #Fonction qui va s'occuper de toutes les actions du joueur
        self.rect = self.image.get_rect()
        self.animation_joueur(display)
        for balle in balles_ennemis : #Regarde s'il se fait toucher par une balle ennemie
            if self.rect.colliderect(balle.rect) :
                self.etat = "mort"
        if self.arme == "tir" :
            self.tick += 1
            if self.tick  < 5 :
                self.animation = 1
                
            elif self.tick == 5 :
                self.arme = "repos"
                self.animation = 0
                self.tick = 0

#Instaciation de la classe Balle
class Balle_Joueur:
    def __init__ (self, x, y ,mouse_x, mouse_y) :
        self.x = x + 15
        self.y = y + 30
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.etat = "tiree"
        self.tick = 0
        #Calcul des angles pour le tir de la balle
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.animation = 0
        self.image = images_balles[self.animation]
        self.rect = self.image.get_rect()
        
    def main(self, display) : #Fonction qui s'occupe des action de la balle
        if self.etat == "tiree" :
            self.x -= int(self.x_vel) #Déplacement de la balle
            self.y -= int(self.y_vel)
        if self.etat == "touchee" :
            self.tick += 1
            if self.tick < 5 :
                self.animation = 1
            elif self.tick < 10 :
                self.animation = 2
        self.image = images_balles[self.animation]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        display.blit(self.image, self.rect)

        
        

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
            balles_ennemis.append(Balle_Ennemi(self.x, self.y, 10))
            self.tick = 0
            self.but_x = random.randint (0, 800)
            self.but_y = random.randint (0, 600)

#Instaciation de la classe Balle

class Balle_Ennemi:
    def __init__ (self, x, y, speed) :
        self.x = x
        self.y = y
        self.speed = speed
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

class Boss :
    def __init__ (self, x, y, width, height) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 4
        self.phase = 3
        self.health = 50
        self.tick = 0
        self.angle = math.atan2(y-player.y, x-player.x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.rota = 0


    def phase1 (self) : 
        self.speed = 15
        if self.tick == 30 :
            self.angle = math.atan2(self.y-player.y, self.x-player.x)
            self.x_vel = math.cos(self.angle) * self.speed
            self.y_vel = math.sin(self.angle) * self.speed
        if (self.tick < 90) and (self.tick > 30) :
            self.x -= int(self.x_vel)
            self.y -= int(self.y_vel)
        if self.tick == 90 :
            self.tick = 0
            self.rota += 1
        if self.rota == 6 :
            self.phase = 2
            self.rota = 0
        
    def phase2 (self) :
        self.speed = 3
        self.angle = math.atan2(self.y-player.y, self.x-player.x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        self.tick += 1
        if self.tick % 20 == 1:
            balles_ennemis.append(Balle_Ennemi(self.x, self.y, 10))
            self.rota += 1
        if self.rota == 50 :
            self.phase = 3
            self.rota = 0
    
    def phase3 (self) :
        self.speed = 0
        self.tick += 1 
        if self.tick == 61 :
            for i in range (20) :
                balles_ennemis.append(Balle_Boss(self.x, self.y, (math.pi/10)*i, 7))
            self.tick = 1
            self.rota += 1
        if self.rota == 10 :
            self.phase = 1
            self.rota = 0


    def main(self, display) :
        pygame.draw.rect(display, (48, 48, 48), (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.phase == 1 :
            self.phase1()
        if self.phase == 2 :
            self.phase2()
        if self.phase == 3 :
            self.phase3()
        self.tick += 1
        if self.rect.colliderect(player.rect) :
            player.etat = "mort"
        for balle in balles_joueur :
            if self.rect.colliderect(balle.rect) :
                self.health -= 1
                balles_joueur.remove(balle)
        
class Balle_Boss:
    def __init__ (self, x, y, angle, speed) :
        self.speed = speed
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        #Calcul des angles pour le tir de la balle
        self.angle = angle
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display) : #Fonction qui s'occupe des action de la balle
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 5)
        self.rect = pygame.Rect(self.x, self.y, 5, 5)

images_balles = [pygame.image.load("Images/BulletProjectile.png"), pygame.image.load("Images/BulletProjectileDissapate1.png"), pygame.image.load("Images/BulletProjectileDissapate2.png")]
images_joueur = [pygame.image.load("Images/MachineGun1.png"), pygame.image.load("Images/MachineGun2.png")]

player= Player(400, 300, 32, 32) #Création du joueur

pos_x = list(range(20, player.x - 100)) + list(range(player.x + 100, 780))
pos_y = list(range(20, player.y - 100)) + list(range(player.y + 100, 580))

positions_objets= [0, 0] #Première valeur = x, deuxième = y. Permet le déplacement de tous les objets autour du joueur

balles_joueur = [] #Permet de gérer l'action de toutes les balles en les ajoutant dans la liste
balles_ennemis = []
ennemis = [] #Permet de gérer l'action de tous les ennemis en les ajoutant à la liste
boss = []
score = 0
tick = 0
vague = 1


myfont = pygame.font.SysFont("monospace", 30)
score_display = myfont.render(str(score), 1, (255,255,0))
display.blit(score_display, (0, 0))
meilleur_score_display =  0
texte_debut = myfont.render(str("Appuyez sur Espace pour commencer"), 1, (0,0,0))
display.blit(texte_debut, (300, 400))
debut = True

ennemis.append(Boss(random.choice(pos_x), random.choice(pos_y), 50, 50))

#Ecran de début
while debut == True :
    display.fill((133, 109, 77)) #remplissage du fond
    score_display = myfont.render(str("Appuyez sur Espace pour commencer"), 1, (0,0,0))
    display.blit(texte_debut, (100, 200))
    
    player.rect.x = player.x
    player.rect.y = player.y
    display.blit(player.image, player.rect)

    for event in pygame.event.get(): #Récupération des evenements
        if event.type == pygame.QUIT : #Permet de quitter proprement pygame
            sys.exit()
    
    keys = pygame.key.get_pressed() #Récupère toutes les touches qui ont été pressées
    if keys[pygame.K_SPACE]:
        debut=False
        
    clock.tick(60) #Permet de faire tourner le jeu à 60 fps
    pygame.display.update() #Update la fenêtre



#Boucle de jeu infinie
while True:
    display.fill((133, 109, 77)) #remplissage du fond
    score_display = myfont.render(str(score), 1, (255,255,0))
    display.blit(score_display, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos() 
    
    """
    if len(ennemis) == 0 :
        vague += 1
        if vague == 21 :
            ennemis.append(Boss(random.choice(pos_x), random.choice(pos_y), 50, 50))
        else:
            for i in range (vague) :
                t_ennemi = random.randint(1, 3)
                if t_ennemi == 1 :
                    ennemis.append(Ennemi(random.choice(pos_x), random.choice(pos_y), 20, 20))
                elif t_ennemi == 2 :
                    ennemis.append(Tireur_Ennemi(random.choice(pos_x), random.choice(pos_y), 20, 20))
                else :
                    ennemis.append(Dash(random.choice(pos_x), random.choice(pos_y), 20, 20))
        vague += 1
    """

    for event in pygame.event.get(): #Récupération des evenements
        if event.type == pygame.QUIT : #Permet de quitter proprement pygame
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN : #Permet de savoir si un bouton de la souris a été pressé
            if event.button == 1:
                balles_joueur.append(Balle_Joueur(player.x, player.y, mouse_x, mouse_y )) #Crée une balle et l'ajoute dans la liste des balles
                player.arme = "tir"
                print("tir")
                player.tick = 0

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
        for boss_2 in boss :
            boss_2.x += 5
        
    if keys[pygame.K_d]:
        positions_objets[0] += 5

        for balle in balles_joueur :
            balle.x -= 5
        for balle in balles_ennemis :
            balle.x -= 5
        for ennemi in ennemis :
            ennemi.x -= 5
        for boss_2 in boss :
            boss_2.x -= 5

    if keys[pygame.K_z]:
        positions_objets[1] -= 5
        
        for balle in balles_joueur :
            balle.y += 5
        for balle in balles_ennemis :
            balle.y += 5
        for ennemi in ennemis :
            ennemi.y += 5
        for boss_2 in boss :
            boss_2.y += 5

    if keys[pygame.K_s]:
        positions_objets[1] += 5

        for balle in balles_joueur :
            balle.y -= 5
        for balle in balles_ennemis :
            balle.y -= 5
        for ennemi in ennemis :
            ennemi.y -= 5
        for boss_2 in boss :
            boss_2.y -= 5

    player.main(display) #Appel de la fonction main qui permet l'action du joueur 
    for balle in balles_joueur: #Appel de la fonction main de toutes les balles
        balle.main(display)
    for ennemi in ennemis: #Appel de la fonction main de tous les ennemis
        ennemi.main(display)
    for balle in balles_ennemis :
        balle.main(display)
    for boss_2 in boss :
        boss_2.main(display)

    for balle in balles_joueur :
        for ennemi in ennemis:
            if balle.rect.colliderect(ennemi.rect) :
                if balle.etat == "tiree" :
                    ennemis.remove(ennemi)
                    balle.etat = "touchee"
                    score += 1
        for balle_e in balles_ennemis :
            if balle.rect.colliderect(balle_e.rect) :
                if balle.etat == "tiree" :
                    ennemis.remove(ennemi)
                    balle.etat = "touchee"
                    score += 1
                    balles_ennemis.remove(balle_e)
        if balle.tick == 10 :
            balles_joueur.remove(balle)
    

    for boss_2 in boss :
        if boss_2.health == 0 :
            boss.remove(boss_2)
    
    file = open("meilleurs_scores.txt", "r+") #Permet de récupérer l'information du meilleur score dans le fichier meilleurs_scores.txt
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
            texte_fin = myfont.render(str("Vous êtes mort"), 1, (0,0,0))
            display.blit(texte_fin, (300, 200))
            
            clock.tick(60) #Permet de faire tourner le jeu à 60 fps
            pygame.display.update() #Update la fenêtre

            for event in pygame.event.get(): #Récupération des evenements
                if event.type == pygame.QUIT : #Permet de quitter proprement pygame
                    bdd_main.enregistrer_score(score)
                    sys.exit()
            
    clock.tick(60) #Permet de faire tourner le jeu à 60 fps
    pygame.display.update() #Update la fenêtre
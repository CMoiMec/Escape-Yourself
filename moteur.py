delta=2# vitesse de descente des platforms
delta2=7# vitesse de descente des astéroides
p2=False# par défaut 1 joueur

class Decor():#élément du décors
    def __init__(self,x,y,l):
        self.x=x#abscisse
        self.y=y#ordonnée
        self.l=l#largeur de l'objet


##le personnage
class Personnage():

    def __init__(self,nom):
        self.nom=nom
        self.x=100#coordonnée
        self.y=350
        self.bx=100#coordonnée précédant
        self.by=350
        self.vx=0#vitesse de x
        self.vy=0#vitesse de y
        self.ax=0
        self.ay=5
        self.dt=0.1
        self.rayon=10
        self.debout=False

    def evoluer(self):
        self.bx,self.by=self.x,self.y
        self.vx=self.vx+self.ax#*self.dt
        self.vy=self.vy+self.ay#*self.dt
        self.x=self.x+self.vx*self.dt
        self.y=self.y+self.vy*self.dt


    def afficher(self):
        print("(x,y): "+str(self.x)+","+str(self.y)+"  vx,vy: "+str(self.vx)+","+str(self.vy))

    def collision(self,obs):
        #renvoie True si les objets sont en collision
        #véréfie les collision dans toutes les directions
        haut=(self.y+self.rayon<=obs.y)
        bas=(self.y-self.rayon>=obs.y+obs.ly)
        gauche=(self.x+self.rayon<=obs.x)
        droite=(self.x-self.rayon>=obs.x+obs.lx)
        collision=not(haut or bas or gauche or droite)
        return collision


class Obstacle():#platform et astéroides

    def __init__(self,dx,dy,dx1,dy1,mechant):
        self.x=dx
        self.y=dy
        self.lx=dx1
        self.ly=dy1
        self.mechant=mechant# True c'est un méchant


##un jeu est un personnage et des obstacles
class Jeu():
    def __init__(self):
        self.pj=[Personnage("p1")]#définie la liste des joueurs à 1
        self.obstacles=[]
        self.background=[]
        self.obstacles+=[Obstacle(50,400,100,10,False)]#platform
        self.obstacles+=[Obstacle(100,300,100,10,False)]
        self.obstacles+=[Obstacle(200,180,100,10,False)]
        self.obstacles+=[Obstacle(250,180,100,10,False)]
        self.obstacles+=[Obstacle(250,130,100,10,False)]
        self.obstacles+=[Obstacle(30,-220,100,10,False)]
        self.obstacles+=[Obstacle(30,-160,100,10,False)]
        self.obstacles+=[Obstacle(300,-90,100,10,False)]
        self.obstacles+=[Obstacle(70,-30,100,10,False)]
        self.obstacles+=[Obstacle(150,0,100,10,False)]
        self.obstacles+=[Obstacle(150,150,20,20,True)]#méchant
        self.obstacles+=[Obstacle(350,20,20,20,True)]#méchant
        self.obstacles+=[Obstacle(450,90,20,20,True)]#méchant
        self.background+=[Decor(0,-450,450)]# décors étoilé
        self.background+=[Decor(0,0,450)]# décors étoilé
        self.background+=[Decor(0,450,450)]# décors étoilé

    def evoluer(self):
        global done,one,score,index_img,direction,direction2,echap
        #évolution du fond
        for image in self.background:
            image.y+=0.5# fait coulisser les images vers le bah
            if image.y>size[1]:# sauf si elle sort intégralement de l'écran
                image.y=-450#alors la recrée tout en haut

        #tous les joueur sont dans les airs
        for i in self.pj:
            i.debout=False

        #deplace les personnages
        for i in self.pj:
            i.evoluer()

        #vérifie qu'aucun des joueurs dans le vide intersidéral de l'espace
        for i in self.pj:
            if i.y>size[1] and len(self.pj)==2:#si l'un des 2 joueurs meurt et qu'il y a 2 joueurs
                done=True# on recommence le jeu
                print("Joueur "+str((not (self.pj.index(i)) )+1 )+" a gagné")# on affiche lequel à survécu le plus longtemps
                return tkt()
            elif i.y>size[1]:#ou sinon 1 joueurs
                done=True# alors recommence le jeu

        for i in self.pj:
            i.y=i.y+delta#fait déscendre le(s) joueur(s) de delta

        for obs in self.obstacles:# pour les platforms et les astéroides
            if not obs.mechant:# si c'est une platform
                obs.y=obs.y+delta# alors la faire tomber de delta
            else:# sinon si c'est un astéroides
                obs.y=obs.y+delta2# les faire tomber rapidement

            for i in self.pj:# pour chaque joueurs
                if (i.collision(obs)):# si le joueur est en collision
                    ##si l'obstacle est mechant on recrée le personnage au début
                    if (obs.mechant):#si c'est un astéroides
                        if p2:#si il y a 2 joueurs
                            print("Joueur "+str((not (self.pj.index(i)) )+1 )+" a gagné")# on affiche lequel des joueurs n'est pas mort
                        done=True
                    else:
                        pj=i
                        if((pj.y<obs.y)and(pj.y+pj.rayon>=obs.y)and (pj.vy>0)) or (pj.vy>0 and pj.by+pj.rayon<=obs.y):##si platform en bas
                            pj.vy=0
                            pj.y=obs.y-pj.rayon
                            ##le personnage est debout sur la platform
                            pj.debout=True

                #recréation d'une platform
                if obs.y> size[1] and not obs.mechant:# si elle est en dehors de la fenètre et que c'est une platform
                    obs.x = randint(0,200)
                    obs.y = -20
                    obs.lx=100
                    score+=100
                    obs.ly=10

                #recréation d'un astéroide
                elif obs.y>700 and obs.mechant:# si elle est en dehors de la fenètre et que c'est un astéroide
                    obs.x = randint(0,450)
                    obs.y = -20
                    obs.lx=20
                    obs.ly=20



        ## --- gestion des evenements et des touches
        for event in pygame.event.get():

            if event.type == pygame.QUIT:# si le joueurs clique sur la croix
                done = True# termine le jeu
                one= True#on ferme la fenètre

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# si echap est préssé
                    echap= not echap # alors on ouvre/ferme le menu

            debout1=self.pj[0].debout#stockage temporaire de chaque joueurs
            debout2=False
            if p2:# si il y a 2 joueurs
                debout2=self.pj[1].debout

            for i in self.pj:#pour chaque personnage

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and debout1:# si le joueur 1 appuie sur haut
                        self.pj[0].vy=-120# alors il saute
                        i.debout=False# et il est dans les airs


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and debout2 and p2:# si le joueurs 2 appuie sur z et qu'il y a bien un second joueurs
                        self.pj[1].vy=-120#alors le joueurs 2 saute
                        i.debout=False#et il est dans les airs

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:#si gauche ou droite sont pressé
                        self.pj[0].vx=0#alors le joueurs est immobile
                        index_img[0]=0#remet l'image 0 du personnage

                if event.type == pygame.KEYUP:
                    if  (event.key == pygame.K_d or event.key == pygame.K_q) and p2:# si q ou d sont pressé par un 2nd joueur
                        self.pj[1].vx=0# alors le joueur 2 est immobile
                        index_img[1]=0#remet l'image 0 du personnage

        ## gestion des évènements et du personnage
        if temp%5==0:#permet de diviser par 5 la vitesse de défilement des images

            for i in self.pj:#pour chaque joueurs
                k = pygame.key.get_pressed()#stock la touche pressé
                #droite
                if  k[pygame.K_RIGHT]:# si c'est la touche droite
                    if self.pj.index(i)==0:# qui est pressé par le joueur 1
                        i.vx=30#se déplace de 30 pixels vers la droite
                        direction = pygame.K_RIGHT #donne la direction du personnage pour savoir quelle image utiliser
                        index_img[0]=(index_img[0]+1)%7#permet le changement d'image du personnage

                #gauche
                if  k[pygame.K_LEFT]:# si c'est la touche gauche
                    if self.pj.index(i)==0:# qui est pressé par le joueur 1
                        i.vx=-30# le Joueur se déplace sur la gauche
                        direction = pygame.K_LEFT# donne la direction du personnage pour savoir quelle image utiliser
                        index_img[0]=(index_img[0]+1)%7# permet le changement d'image du personnage

                if  k[pygame.K_d] and p2:# si la c'est la touche d qui est pressé et qu'il existe un 2nde joueur
                    if self.pj.index(i)==1:# qui est pressé par le joueur 2
                        i.vx=30# le joueur se déplace vers la droite
                        direction2 = pygame.K_d# donne la direction du personnage pour savoir quelle image  utiliser
                        index_img[1]=(index_img[1]+1)%7# permet le chnagement d'image du personnage

                #gauche
                if  k[pygame.K_q] and p2:# si la c'est la touche q qui est pressé et qu'il existe un 2nde joueur
                    if self.pj.index(i)==1:# qui est pressé par le joueur 2
                        i.vx=-30#  le joueur se déplace vers la gauche
                        direction2 = pygame.K_q# donne la direction du personnage pour savoir quelle image  utiliser
                        index_img[1]=(index_img[1]+1)%7# permet le chnagement d'image du personnage



    def dessiner(self):
        #définiton des couleurs
        WHITE = (0xFF, 0xFF, 0xFF)
        RED = (0xFF, 0x00, 0x00)
        BLUE = (0x00, 0x00, 0xFF)
        BLACK = (0x00, 0x00, 0x00)
        GREEN = (0x00, 0xFF, 0x00)
        screen.fill(WHITE)# remplie le fond en blanc

        #dessin du fond
        for image in self.background:
            screen.blit(bg,(image.x,image.y))#affiche les images en fond



        #dessin du score
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(score), True, RED)
        screen.blit(img, (20, 20))

        ##dessin obstacle
        for obs in self.obstacles:
            if (obs.mechant):
                screen.blit(meteor,(obs.x-5,obs.y-5,obs.lx,obs.ly))#dessine un astéroide
            else:
                screen.blit(plat,(obs.x,obs.y,obs.lx,obs.ly))#dessine une platform

        ##dessin personnage
        for i in self.pj:
            rayon=i.rayon
            if self.pj.index(i) == 0:# dessin du joueur 1
                image_animation[direction][index_img[0]]=pygame.transform.scale(image_animation[direction][index_img[0]], (4*rayon,4*rayon))
                screen.blit(image_animation[direction][index_img[0]],(i.x-(rayon+10) ,i.y-(rayon+17)))
            else:#dessin du joueur 2
                image_animation[direction2][index_img[1]]=pygame.transform.scale(image_animation[direction2][index_img[1]], (4*rayon,4*rayon))
                screen.blit(image_animation[direction2][index_img[1]],(i.x-(rayon+10) ,i.y-(rayon+17)))



#importation des bibliothèque
from random import randint
from test import *
import pygame

#initialisation des paramètres de pygame
pygame.init()
size = (300, 700)#dimensions de la fenètre
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Escape Yourself")#nom jeu
clock = pygame.time.Clock()

#chargement des images
plat=pygame.image.load("assets/platform.png")
bg=pygame.image.load("assets/fond.png")
meteor=pygame.image.load("assets/meteor.png")
perso = pygame.image.load('assets/sprite.png')
perso2 =pygame.image.load('assets/sprite2.png')

#découpage du personnage
image_animation = {pygame.K_RIGHT:[perso.subsurface(x,0,17,21)for x in range(0,119,17)],# dictionnaire associant le nom des touches a la decoupe de 4 image
                   pygame.K_LEFT:[perso.subsurface(x,24,17,21)for x in range(0,119,17)],
                   pygame.K_d:[perso2.subsurface(x,0,17,21)for x in range(0,119,17)],
                   pygame.K_q:[perso2.subsurface(x,24,17,21)for x in range(0,119,17)]
                   }


direction = pygame.K_RIGHT# orientation du joueur 1
direction2 = pygame.K_d#orientation du joueur 2
index_img = [0,0]#indice des images des joueurs
bscore=0#le meilleurs est de 0 au départ

def menu():
    global echap,done,one,p2

    #paramètres du menu
    GREEN = (0x00, 0xFF, 0x00)
    font = pygame.font.SysFont(None, 24)
    img1 = font.render("Echap: Pause", True, GREEN)
    img2 = font.render("1: Mode 1 Joueur", True, GREEN)
    img3 = font.render("2: Mode 2 joueur(ZQD)", True, GREEN)

    #impression du menu
    screen.blit(img1, (20, 40))
    screen.blit(img2, (20, 60))
    screen.blit(img3, (20, 80))
    pygame.display.flip()

    #permet de mettre en pause le Jeu
    while echap:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# si la touche echap es pressé
                    echap= not echap#alors on quitte le menu

            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_1:# la touche 1 est pressé
                    p2=False#alors pas de 2nde joueurs
                    done=True# recommence le jeu
                    echap=False#on quitte le menu

            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_2:#si la touche 2 est pressé
                    p2=True#alors un 2nd joueur
                    done=True#on relnace le jeu
                    echap=False#on quitte le menu

            if event.type == pygame.QUIT:# si la croix est pressé
                done = True#on relance le jeu
                one= True#on ferme le jeu
                echap=False#on quitte le menu

def tkt():
    global jeu,score,temp

    ##creation du jeu à 1 ou 2 joueurs

    jeu=Jeu()
    if p2:
        jeu.pj=[Personnage("p1"),Personnage("p2")]
    score=0#score de la manche à 0
    temp=0# permet de réguler les images des personnages

    return tkt1()

def tkt1():
    global done,one,bscore,temp,echap

    one=False#permet de quitter le jeu
    done = False# permet de reset le jeu
    echap=False# permet d'afficher le menu

    ## -------- boucle principale
    while not done:

        ## --- evolution du jeu
        jeu.evoluer()

        ## --- affichage
        jeu.dessiner()

        if echap:# si échape est pressé
            menu()# on appelle le menu

        ## --- mise a jour graphique
        pygame.display.flip()
        temp+=1
        ## --- attente
        clock.tick(60)

    if done and not one:# si on relance le jeu
        if score>bscore:# et si amélioration du score
            bscore=score#alors c'est le meilleur score
        return tkt()#recréation du jeu
tkt()#lance la création du jeu

pygame.quit()#on quitte pygame
print(bscore)#on affiche le meilleur score de la partie

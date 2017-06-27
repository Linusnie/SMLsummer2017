#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# server_gui.py

#############################################################################
# Copyright (C) Labomedia February 2015
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

import pygame
import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3, PoseArray, Pose
from turtlesim.msg import Pose as Pos
import datetime
from nav_msgs.msg import Odometry
from pygame.locals import *


pygame.init()
clock = pygame.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
CIEL = 0, 200, 255
RED = 255, 0, 0
ORANGE = 255, 100, 0
GREEN = 0, 255, 0
GREEN2 = 32, 178, 15
LIGHTBLUE = 202, 237, 233


#Initialize ROS node
rospy.init_node('GUIControl', anonymous=True)

#Initialize global variables
V=None
X=None
Y=None
Tableau2=[]

#Define the subscriber to the velocity
def callbackVel(msg):
    global V
    #rospy.loginfo("Received a /cmd_vel message!")
    #rospy.loginfo(rospy.get_caller_id()+"I heard %s", Twist.linear)
    #rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    #rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
    #rospy.loginfo("Conversion : x lineaire : [%f], x converti: [%f]" %(msg.linear.x, msg.linear.x*10))
    V=msg.linear.x
    
Subs=rospy.Subscriber("/turtle1/cmd_vel", Twist, callbackVel)

#Define the subscriber to the position
def callbackPose(msg):
    global X, Y
    #rospy.loginfo("Received a /Pose message !!")
    #rospy.loginfo("Position de la tortue : [%f, %f]" %(msg.x, msg.y) )
    X=msg.x
    Y=msg.y

SubsPose=rospy.Subscriber("/turtle1/pose", Pos, callbackPose)

#Define the subscriber to the position
def callbackCar_State(msg):
    #global X, Y
    #rospy.loginfo("Received a /Pose message !!")
    #rospy.loginfo("Position de la tortue : [%f, %f]" %(msg.x, msg.y) )
    return

SubsCar_State=rospy.Subscriber("/car_state_topic", Odometry, callbackCar_State)

#Initialize publisher of the waypoints
goalPublisher=rospy.Publisher('waypoints', PoseArray, queue_size=10)

#Date 
date=datetime.datetime.now()


#Waypoints coordinates
Tableau1=[[995, 789], [995, 670], [995, 550],[995, 802], [995, 728], [995, 200],[995, 127],[995, 186],[995, 217],[995, 42]]
print(len(Tableau1))

class Button:
    '''Ajout d'un bouton avec un texte sur img
    Astuce: ajouter des espaces dans les textes pour avoir une même largeur
    de boutons
    dx, dy décalage du bouton par rapport au centre
    action si click
    Texte noir
    '''

    def __init__(self, fond, text, color, font, dx, dy):
        self.fond = fond
        self.text = text
        self.color = color
        self.font = font
        self.dec = dx, dy
        self.state = False  # enable or not
        self.title = self.font.render(self.text, True, BLACK)
        textpos = self.title.get_rect()
        textpos.centerx = self.fond.get_rect().centerx + self.dec[0]
        textpos.centery = self.dec[1]
        self.textpos = [textpos[0], textpos[1], textpos[2], textpos[3]]
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)
        


    def update_button(self, fond, action=None):
        self.fond = fond
        mouse_xy = pygame.mouse.get_pos()
        over = self.rect.collidepoint(mouse_xy)
        if over:
            action()
            if self.color == RED:
                self.color = GREEN
                self.state = True
            elif self.color == GREEN:
                # sauf les + et -, pour que ce soit toujours vert
                if len(self.text) > 5:  # 5 char avec les espaces
                    self.color = RED
                self.state = False
        # à la bonne couleur
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)

    def display_button(self, fond):
        self.fond = fond
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.title, self.textpos)


class Game:
    def __init__(self, *args):
        self.screen = pygame.display.set_mode((1571, 872))
        self.level = 0.0 
        self.loop = True
        self.position_perso=(600,600)
        self.status = 'Waiting to begin'
        self.scale=1
        # Définition de la police
        self.big = pygame.font.SysFont('freesans', 48)
        self.small = pygame.font.SysFont('freesans', 36)
        self.mediumsmall = pygame.font.SysFont('freesans',28)
        self.verysmall = pygame.font.SysFont('freesans', 10)

        self.create_fond()
        self.create_button()

    def update_textes(self):
        self.textes = [ ["Autonomous Driving with F1/10", ORANGE, self.small, 0, 50],
                        ["Speed :", BLACK, self.small, -110, 150],
                        [str(self.level), BLACK, self.small, 0, 150],
                        ["Status :", BLACK, self.small, -110, 250],
                        [str(self.status), BLACK, self.small, 70, 250],
                        ["Destination :", BLACK, self.small, -70, 350],
                        ["Maps :", BLACK, self.small, -110, 450],
                        ["KTH Campus, Stockholm", BLACK, self.verysmall, 160, 840],
                        ["OpenStreetMap ", BLACK, self.verysmall, 142, 850],
                        [str(date), BLACK, self.verysmall, 172, 861]]
    def create_fond(self):
        # Image de la taille de la fenêtre
        self.fond = pygame.Surface((500, 872))
        # En bleu
        self.fond.fill(WHITE)

    def create_button(self):
        self.reset_button = Button(self.fond, "   Reset   ", RED, self.small, -90, 700)
        self.start_button = Button(self.fond, "    Start    ", RED, self.small, -89, 745)
        self.quit_button  = Button(self.fond, "   Quit   ", RED, self.small, -200, 853)
        self.moins_button = Button(self.fond, "  -  ", GREEN, self.small, 30, 700)
        self.plus_button  = Button(self.fond, "  +  ", GREEN, self.small, 30, 745)
        self.Scenario1_button = Button(self.fond, "  Scenario 1  ", LIGHTBLUE, self.small, -60, 550)
        self.Scenario2_button=Button(self.fond,"  Scenario 2  ", CIEL, self.small, -60,595)
        self.Kista_button = Button(self.fond, "  Kista  ", LIGHTBLUE, self.small, 130, 450)
        self.KTH_button = Button(self.fond, "  KTH  ", LIGHTBLUE, self.small, 10, 450)
        self.EraseScenario1_button = Button(self.fond, "  Erase  ", LIGHTBLUE, self.small, 200, 550)
        self.PersoScenario_button = Button(self.fond, "  Customized Scenario  ", LIGHTBLUE, self.small, -60, 650)

    def display_text(self, text, color, font, dx, dy):
        '''Ajout d'un texte sur fond. Décalage dx, dy par rapport au centre.
        '''
        mytext = font.render(text, True, color)  # True pour antialiasing
        textpos = mytext.get_rect()
        textpos.centerx = self.fond.get_rect().centerx + dx
        textpos.centery = dy
        self.fond.blit(mytext, textpos)

    

    def Display_KistaMap(self):
        KistaMap=pygame.image.load('mapKista.png').convert()
        self.screen.blit(KistaMap, (500,0))
        self.map='KistaMap'
        pygame.display.update()

    def Display_KTHMap(self):
        KTHMap=pygame.image.load('mapKTH.png').convert()
        self.screen.blit(KTHMap, (500,0))
        self.map='KTHMap'
        pygame.display.update()

    def plus(self):
        KistaMap=pygame.image.load('mapKista.png').convert()
        KTHMap=pygame.image.load('mapKTH.png').convert()
        self.scale+=0.5
        if self.map=='KistaMap':
            KistaMap=pygame.transform.rotozoom(KistaMap, 0, self.scale)
            self.screen.blit(KistaMap, (500,0))
        elif self.map=='KTHMap':
            KTHMap=pygame.transform.rotozoom(KTHMap, 0, self.scale)
            self.screen.blit(KTHMap, (500,0))
        pygame.display.update()
        print('+')

    def moins(self):
        KistaMap=pygame.image.load('mapKista.png').convert()
        KTHMap=pygame.image.load('mapKTH.png').convert()
        if self.scale>1 :
            self.scale-=0.5
        if self.map=='KistaMap':
            KistaMap=pygame.transform.rotozoom(KistaMap, 0, self.scale)
            self.screen.blit(KistaMap, (500,0))
        elif self.map=='KTHMap':
            KTHMap=pygame.transform.rotozoom(KTHMap, 0, self.scale)
            self.screen.blit(KTHMap, (500,0))
        pygame.display.update()
        print('-')
    
    def Scenario1(self):
        #Displays the waypoints of scenario 1
        
        for i in range (len(Tableau1)):
            x,y=Tableau1[i][0], Tableau1[i][1]
            pygame.draw.circle(self.screen, ORANGE, (x,y), 5, 0)
            print(i)
        waypointsPublish()


    def CreatePersonalizedScenario(self):
        #Create waypoints by mouse clicking on the map;
        #Press Return to stop the selection 
        #Add restriction if the click is not on the map
        #x,y : position relative to the left corner of the display
       
        continuer=1
        while continuer:
            for event in pygame.event.get():
                print('Get a event msg')
                if event.type==MOUSEBUTTONDOWN and event.button==1:
                    print('Get a mousebutton msg')
                    x,y=pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                    P=[x,y]
                    Tableau2.extend([P])
                    pygame.draw.circle(self.screen, ORANGE, (x,y), 5, 0)
                    pygame.display.update()
                print(Tableau2)
                if event.type==KEYDOWN :
                    if event.key==K_RETURN:
                        waypoints_personalized()
                        continuer=0
        


    def infinite_loop(self):
        #Caracteristiques de la carte #faire un input
        #KTHMap
        LongitMin=18.06208
        LongitMax=18.07555
        LatitMin=59.34838
        LatitMax=59.35397
        fenetreWidth=1071
        fenetreHeight=872
        EchelleLongit=((LongitMax-LongitMin)/fenetreWidth)
        EchelleLatit=((LatitMax-LatitMin)/fenetreHeight)

        #KistaMap
        LongitMin=17.95017
        LongitMax=17.95354
        LatitMin=59.40374
        LatitMax=59.40517
        fenetreWidth=1071
        fenetreHeight=872
        EchelleLongit=((LongitMax-LongitMin)/fenetreWidth)
        EchelleLatit=((LatitMax-LatitMin)/fenetreHeight)


        while self.loop:
            self.create_fond()

            #Mise a jour de la valeur de la vitesse
            #print(V)
            self.level=V

            #Update the status
            self.status="No subscriber"

            #if X!=None and Y!=None:
            #    x=int(((X-LongitMin)/EchelleLongit))
            #    y=int(((LatitMax-Y)/EchelleLatit))
            #    position_perso.centerx=x
            #    position_perso.centery=y
            #    print(position_perso.centerx, position_perso.centery)

            # Boutons
            self.reset_button.display_button(self.fond)
            self.start_button.display_button(self.fond)
            self.quit_button.display_button(self.fond)
            self.moins_button.display_button(self.fond)
            self.plus_button.display_button(self.fond)
            self.Scenario1_button.display_button(self.fond)
            self.Scenario2_button.display_button(self.fond)
            self.Kista_button.display_button(self.fond)
            self.KTH_button.display_button(self.fond)
            self.EraseScenario1_button.display_button(self.fond)
            self.PersoScenario_button.display_button(self.fond)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_button.update_button(self.fond, action=reset)
                    self.start_button.update_button(self.fond, action=start)
                    self.quit_button.update_button(self.fond, action=gamequit)
                    self.moins_button.update_button(self.fond, action=self.moins)
                    self.plus_button.update_button(self.fond, action=self.plus)
                    self.Scenario1_button.update_button(self.fond, action=self.Scenario1)
                    self.Scenario2_button.update_button(self.fond, action=waypointsPublish2)
                    self.Kista_button.update_button(self.fond, action=self.Display_KistaMap)
                    self.KTH_button.update_button(self.fond, action=self.Display_KTHMap)
                    self.EraseScenario1_button.update_button(self.fond, action=self.Display_KTHMap)
                    self.PersoScenario_button.update_button(self.fond, action=self.CreatePersonalizedScenario)

            self.update_textes()
            for text in self.textes:

                self.display_text(text[0], text[1], text[2],
                                        text[3], text[4])

            # Ajout du fond dans la fenêtre
            self.screen.blit(self.fond, (0, 0))

            #Ajout de la carte
            #self.fond2=pygame.Surface((1000, 872))
            #self.screen.blit(self.fond2,(500,0))
            #map=pygame.image.load('map.png').convert()
            #self.screen.blit(map, (500,0))

            #Load the moving point picture
            perso=pygame.image.load('square.png').convert()
            self.position_perso=perso.get_rect()
            #print(self.position_perso)

            #print('Valeur de X', X, 'Valeur de Y', Y)

            if X!=None and Y!=None: 
                self.position_perso=[(X*(1071/11.08)+500), (Y*(-872/11.08)+872)]
            #print('position_perso', position_perso)

            self.screen.blit(perso, self.position_perso)
            #print(self.position_perso)
            
            # Actualisation de l'affichage
            pygame.display.update()
            # 10 fps
            clock.tick(5)


def reset():
    print("reset")

def start():
    print("start")

def gamequit():
    print("Quit")
    pygame.quit()
    sys.exit()



def waypointsPublish():
#Starts publishing 10 waypoints on the topic 'waypoints'
#It publishes once at the mousebutton click
#Tableau1=[[Xi,Yi]i], waypoints coordinates 
    point1, point2, point3, point4, point5, point6, point7, point8, point9, point10 =Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose()
    Array=PoseArray()

    point1.position.x, point1.position.y=Tableau1[0][0],Tableau1[0][1]
    point2.position.x, point2.position.y=Tableau1[1][0],Tableau1[1][1]
    point3.position.x, point3.position.y=Tableau1[2][0],Tableau1[2][1]
    point4.position.x, point4.position.y=Tableau1[3][0],Tableau1[3][1]
    point5.position.x, point5.position.y=Tableau1[4][0],Tableau1[4][1]
    point6.position.x, point6.position.y=Tableau1[5][0],Tableau1[5][1]
    point7.position.x, point7.position.y=Tableau1[6][0],Tableau1[6][1]
    point8.position.x, point8.position.y=Tableau1[7][0],Tableau1[7][1]
    point9.position.x, point9.position.y=Tableau1[8][0],Tableau1[8][1]
    point10.position.x, point10.position.y=Tableau1[9][0],Tableau1[9][1]

    Array.poses.extend((point1, point2, point3, point4, point5, point6, point7, point8, point9, point10))
    
    rospy.loginfo(Array)
    goalPublisher.publish(Array)


    #rate=rospy.Rate(10)
    #rate.sleep()
def waypoints_personalized():
    #Publishes the waypoints coming from the personalized scenario
    #Assumes that the max number of waypoints is 10. There is an undetermined number of waypoints which are treated with the list Stock.
    
    print('Waypoints Personalized')
    NbrePoints=len(Tableau2)
    point1, point2, point3, point4, point5, point6, point7, point8, point9, point10 =Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose(), Pose()
    Array=PoseArray()
    Stock=[point1, point2, point3, point4, point5, point6, point7, point8, point9, point10]

    for i in range (NbrePoints):
        Stock[i].position.x,Stock[i].position.y=Tableau2[i][0],Tableau2[i][1]
        
    Array.poses.extend((Stock[i]) for i in range(NbrePoints))
        
    rospy.loginfo(Array)
    goalPublisher.publish(Array)

def waypointsPublish2():
    print 'Scenario 2'

if __name__ == '__main__':
    game = Game()
    game.infinite_loop()

   
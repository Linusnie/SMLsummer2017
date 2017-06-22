#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion, Vector3
import numpy as np
from Tkinter import *
import os
import pygame
from pygame.locals import *


#Affiche une carte, une croix et une fleche
#La fleche est orientee selon l'orientation de la voiture par communication ROS
#La croix et la fleche devront se deplacer sur la carte par souscription a 
#un autre topic ROS

pygame.init()

fenetreWidth=1071
fenetreHeight=872

#Background
fenetre=pygame.display.set_mode((fenetreWidth,fenetreHeight))
fond=pygame.image.load('map.png').convert()
fenetre.blit(fond,(0,0))

#Cross
perso=pygame.image.load('croix.png').convert()
position_perso=perso.get_rect() 
position_perso.centery=fond.get_rect().centery
position_perso.centerx=fond.get_rect().centerx 
fenetre.blit(perso,position_perso)

#Arrow
fleche=pygame.image.load('fleche.jpg').convert()
fleche=pygame.transform.scale(fleche, (75,75))

pygame.key.set_repeat(400, 30)

pygame.display.flip()
#raifraichissement de lecran pour voir les modifications et limage safficher 
continuer=1


#Caracteristiques de la carte
LongitMin=18.06208
LongitMax=18.07555
LatitMin=59.34838
LatitMax=59.35397
EchelleLongit=((LongitMax-LongitMin)/fenetreWidth)
EchelleLatit=((LatitMax-LatitMin)/fenetreHeight)



def callbackIMU(msg):
	rospy.loginfo("Received a Quaternion message !! Ready to calculate the orientation")
	rospy.loginfo("Orientation x, y : [%f, %f]" %(msg.orientation.x, msg.orientation.y) )
	#ou juste msg.x et msg.y ?

	#Calcul de l'angle de rotation theta
	x=msg.orientation.x
	y=msg.orientation.y
	theta=np.arctan((y/x))

	#Rotation de l'image fleche
	fleche=pygame.transform.rotate(fleche, theta)
	fleche.set_colorkey((255,255,255))

	rospy.loginfo("Received a Vector 3 message !! Ready to calculate the speed")
	rospy.loginfo("Linear acceleration x, y: [%f, %f]" %(msg.linear_acceleration.x, msg.linear_acceleration.y))

	#Integration pour la vitesse


	#Affichage 
	fenetre.blit(fond,(0,0))
	fenetre.blit(fleche,(150,150))
	position_perso=[150,150]
	fenetre.blit(perso,position_perso)
	pygame.display.update()
	


def IMU_Subscriber_HMI():
	rospy.init_node('IMU_Subscriber_HMI')
	rospy.Subscriber("/imu", Quaternion, callbackIMU)
	rospy.spin()


#def callbackGPS(msg):
#	rospy.loginfo('Received message from the GPS')
#	latitude=msg.somtething
#	longitude=msg.somtething

	#Conversion pixel : definition de la position sur l'ecran
#	x=int(((Longitude-LongitMin)/EchelleLongit))
#	y=int(((LatitMax-Latitude)/EchelleLatit))

	#Affichage du point
#	position_perso.centerx=x
#	position_perso.centery=y
#	fenetre.blit(perso,position_perso)
#	pygame.display.update()
#	pygame.time.delay(2)

#def GPS_Subscriber_HMI():
#	rospy.init_node('GPS_Subscriber_HMI')
#	rospy.Subscriber("", ,callbackGPS)
#	rospy.spin()


class Application(Frame):
    #def say_hi(self):
    #   print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.grid(row=13, column=9)

        self.Sc1 = Button(self)
        self.Sc1["text"] = "Scenario 1",
        self.Sc1.grid(row=5, column=9)
        #self.Sc1["command"] = self.say_hi

        self.Sc2 = Button(self)
        self.Sc2["text"] = "Scenario 2",
        self.Sc2.grid(row=7, column=9)

        self.Sc3 = Button(self)
        self.Sc3["text"] = "Scenario 3",
        self.Sc3.grid(row=9, column=9)

        self.Speed=Label(self)
        self.Speed["text"]="Speed :"
        self.Speed.grid(row=2, column=2)

        self.Status=Label(self)
        self.Status["text"]="Status :"
        self.Status.grid(row=3, column=2)

        self.Destination=Label(self)
        self.Destination["text"]="Destination :"
        self.Destination.grid(row=4, column=2)

        #TitleFont=font.Font(family='Arial', size='18', weight='bold')
        self.Title=Label(self)
        self.Title["text"]="Autonomous Driving With F1/10"
        #self.Title["font"]=TitleFont
        self.Title.grid(row=1, column=4)



    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



if __name__=='__main__':
	IMU_Subscriber_HMI()

	root = Tk()
	app = Application(master=root)
	app.mainloop()
	root.destroy()

	while continuer :
	   for event in pygame.event.get(): #on parcourt la liste de tous les evenements recus
	       if event.type==QUIT:         #si lun de ces evenements est de type QUIT
		      continuer=0 
	
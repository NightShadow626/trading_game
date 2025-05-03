import os
import pygame
import random


# pour le son
pygame.mixer.init()


# Lancer la lecture des musiques
pygame.mixer.music.stop()

# Fonction pour jouer les musiques de façon aléatoire et en boucle
def jouer_musiques(titre):
    # Mélanger les fichiers musicaux et les jouer en boucle
    pygame.mixer.music.load(titre)
    pygame.mixer.music.set_volume(0.5)  # Volume entre 0.0 et 1.0
    pygame.mixer.music.play()

def ajuster_volume(volume):
    pygame.mixer.music.set_volume(float(volume))
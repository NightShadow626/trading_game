# -*- coding: utf-8 -*-
# importation des modules nécessaires
import pygame

# pour le son
pygame.mixer.init()

# stoper ce qui est eventuellement en cours
pygame.mixer.music.stop()

# Fonction pour jouer les musiques de façon aléatoire et en boucle
def jouer_musiques(titre : str) -> None:
    '''Joue la musique spécifiée en boucle.'''
    # Mélanger les fichiers musicaux et les jouer en boucle
    pygame.mixer.music.load(titre)
    pygame.mixer.music.set_volume(0.5)  # Volume entre 0.0 et 1.0
    pygame.mixer.music.play()

def ajuster_volume(volume : float) -> None:
    '''Ajuste le volume de la musique.'''
    # Ajuster le volume de la musique
    # Le volume doit être entre 0.0 et 1.0
    if volume < 0.0 or volume > 1.0:
        raise ValueError("Le volume doit être compris entre 0.0 et 1.0")
    pygame.mixer.music.set_volume(float(volume))
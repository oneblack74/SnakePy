# ######################################################################################################################
# IMPORTATIONS
# ######################################################################################################################


import pygame
import game
from constantes import *
from functions import dessiner_menu_debut, dessiner_menu_fin
from menu import affiche_menu
pygame.init()


# ######################################################################################################################
# FONCTION PRINCIPALE
# ######################################################################################################################


def main():
    # Création de la fenêtre de jeu
    root = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Snake")

    # Menu début
    menu_choix = affiche_menu(root, dessiner_menu_debut(root))  # 0 -> quitter | 1 -> jouer

    # Boucle de menu
    while menu_choix == 1:

        # Création du snake
        snake = game.init()

        # Lancement du jeu
        sortie = game.play(root, snake)

        if sortie == 0:
            break
        elif sortie == 2:
            # Afficher menu perdu
            menu_choix = affiche_menu(root, dessiner_menu_fin(root, 0))
        elif sortie == 3:
            # Afficher menu gagné
            menu_choix = affiche_menu(root, dessiner_menu_fin(root, 1))

    # Quitte la fenêtre
    pygame.quit()


# ######################################################################################################################
# LANCEMENT AUTOMATIQUE
# ######################################################################################################################


if __name__ == "__main__":
    main()

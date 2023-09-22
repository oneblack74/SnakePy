# ######################################################################################################################
# IMPORTATIONS
# ######################################################################################################################


import pygame
from constantes import *
from functions import dessiner_menu_debut, dessiner_menu_fin, dessiner_contour


# ######################################################################################################################
# FONCTIONS
# ######################################################################################################################


# ----------------------------------------------------------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------------------------------------------------------


def affiche_menu(surface, liste_menu):
    """
    :param surface:
    :param liste_menu:
    :return: int
    """
    # Boucle de menu
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                return 0
            if event.type == pygame.KEYDOWN:
                # Vers le haut
                if event.key in [pygame.K_UP, pygame.K_z]:
                    aucun = True
                    for i in range(len(liste_menu)):
                        if liste_menu[i]["etat"]:
                            if i > 0:
                                liste_menu[i]["etat"] = False
                                dessiner_contour(surface, liste_menu[i], COULEUR_FOND)
                                liste_menu[i - 1]["etat"] = True
                                dessiner_contour(surface, liste_menu[i - 1], COULEUR_TEXTE)
                            aucun = False
                            break
                    if aucun:
                        liste_menu[0]["etat"] = True
                        dessiner_contour(surface, liste_menu[0], COULEUR_TEXTE)
                # Vers le bas
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    aucun = True
                    for i in range(len(liste_menu)):
                        if liste_menu[i]["etat"]:
                            if i < (len(liste_menu) - 1):
                                liste_menu[i]["etat"] = False
                                dessiner_contour(surface, liste_menu[i], COULEUR_FOND)
                                liste_menu[i + 1]["etat"] = True
                                dessiner_contour(surface, liste_menu[i + 1], COULEUR_TEXTE)
                            aucun = False
                            break
                    if aucun:
                        liste_menu[len(liste_menu) - 1]["etat"] = True
                        dessiner_contour(surface, liste_menu[len(liste_menu) - 1], COULEUR_TEXTE)
                # Entrée
                if event.key == pygame.K_RETURN:
                    for choix in liste_menu:
                        if choix["etat"]:
                            return choix["valeur"]
            if event.type == pygame.MOUSEMOTION:
                for choix in liste_menu:
                    if not choix["etat"]:
                        if ((pygame.mouse.get_pos()[0] >= (choix["coord"][0] - CADRE_GAP)) and (pygame.mouse.get_pos()[0] <= (choix["coord"][0] + choix["largeur"] + CADRE_GAP))) \
                                and ((pygame.mouse.get_pos()[1] >= (choix["coord"][1] - CADRE_GAP)) and (pygame.mouse.get_pos()[1] <= (choix["coord"][1] + choix["hauteur"] + CADRE_GAP))):
                            for choix_bis in liste_menu:
                                if choix_bis["etat"]:
                                    choix_bis["etat"] = False
                                    dessiner_contour(surface, choix_bis, COULEUR_FOND)
                                    break
                            choix["etat"] = True
                            dessiner_contour(surface, choix, COULEUR_TEXTE)
            if pygame.mouse.get_pressed(3)[0]:
                for choix in liste_menu:
                    if choix["etat"]:
                        if ((pygame.mouse.get_pos()[0] >= (choix["coord"][0] - CADRE_GAP)) and (pygame.mouse.get_pos()[0] <= (choix["coord"][0] + choix["largeur"] + CADRE_GAP))) \
                                and ((pygame.mouse.get_pos()[1] >= (choix["coord"][1] - CADRE_GAP)) and (pygame.mouse.get_pos()[1] <= (choix["coord"][1] + choix["hauteur"] + CADRE_GAP))):
                            return choix["valeur"]

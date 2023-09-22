# ######################################################################################################################
# IMPORTATIONS
# ######################################################################################################################


import pygame
from constantes import *
import random


# ######################################################################################################################
# FONCTIONS
# ######################################################################################################################


# ----------------------------------------------------------------------------------------------------------------------
# Serpent
# ----------------------------------------------------------------------------------------------------------------------


def dessiner_tete(snake, surface, coord):
    """
    :param snake:
    :param surface:
    :param coord:
    :return: None
    """
    if snake["corps"][-1]["direction"] == "haut":
        afficher(surface, snake["images"]["haut"], coord)
    elif snake["corps"][-1]["direction"] == "bas":
        afficher(surface, snake["images"]["bas"], coord)
    elif snake["corps"][-1]["direction"] == "droite":
        afficher(surface, snake["images"]["droite"], coord)
    elif snake["corps"][-1]["direction"] == "gauche":
        afficher(surface, snake["images"]["gauche"], coord)


def dessiner_snake(snake, surface):
    """
    :param snake:
    :param surface:
    :return: None
    """
    # Dessiner le corps
    for partie in snake["corps"][:-1]:
        pygame.draw.rect(surface, COULEUR_SNAKE, (partie["x"], partie["y"], BOX_SIZE, BOX_SIZE))
    # Dessiner la tête
    if snake["corps"][-1]["direction"] == "haut":
        dessiner_tete(snake, surface, (snake["corps"][-1]["x"], snake["corps"][-1]["y"] + (BOX_WIDTH - snake["compteur"])))
    elif snake["corps"][-1]["direction"] == "bas":
        dessiner_tete(snake, surface, (snake["corps"][-1]["x"], snake["corps"][-1]["y"] - (BOX_WIDTH - snake["compteur"])))
    elif snake["corps"][-1]["direction"] == "gauche":
        dessiner_tete(snake, surface, (snake["corps"][-1]["x"] + (BOX_WIDTH - snake["compteur"]), snake["corps"][-1]["y"]))
    elif snake["corps"][-1]["direction"] == "droite":
        dessiner_tete(snake, surface, (snake["corps"][-1]["x"] - (BOX_WIDTH - snake["compteur"]), snake["corps"][-1]["y"]))
    # Dessiner carré noir
    if snake["pomme_attente"] < 1:
        if snake["corps"][1]["direction"] == "haut":
            pygame.draw.rect(surface, COULEUR_FOND, (snake["corps"][0]["x"], snake["corps"][0]["y"] + BOX_WIDTH - snake["compteur"], BOX_SIZE, snake["compteur"]))
        elif snake["corps"][1]["direction"] == "bas":
            pygame.draw.rect(surface, COULEUR_FOND, (snake["corps"][0]["x"], snake["corps"][0]["y"], BOX_SIZE, snake["compteur"]))
        elif snake["corps"][1]["direction"] == "gauche":
            pygame.draw.rect(surface, COULEUR_FOND, (snake["corps"][0]["x"] + BOX_WIDTH - snake["compteur"], snake["corps"][0]["y"], snake["compteur"], BOX_SIZE))
        elif snake["corps"][1]["direction"] == "droite":
            pygame.draw.rect(surface, COULEUR_FOND, (snake["corps"][0]["x"], snake["corps"][0]["y"], snake["compteur"], BOX_SIZE))
    elif snake["compteur"] == BOX_WIDTH:
        snake["pomme_attente"] -= 1

# ----------------------------------------------------------------------------------------------------------------------
# Pomme
# ----------------------------------------------------------------------------------------------------------------------


def nouvelle_pomme(snake):
    """
    :param snake:
    :return: tuple(int, int)
    """
    colonne, ligne = -1, -1
    valide = False
    while not valide:
        colonne = random.randint(0, BOX_WIDTH - 1) * BOX_SIZE + WIN_BORDER
        ligne = random.randint(0, BOX_HEIGHT - 1) * BOX_SIZE + WIN_BORDER
        if (colonne, ligne) not in [(partie["x"], partie["y"]) for partie in snake["corps"]]:
            valide = True
    return colonne, ligne


def ecrire_texte_pomme(snake, police, surface):
    """
    :param snake:
    :param police:
    :param surface:
    :return: None
    """
    texte = police.render(str(snake["pomme"]), True, COULEUR_TEXTE, COULEUR_WIN_TEXT)
    afficher(surface, texte, (WIN_WIDTH - WIN_TEXT / 2 - texte.get_width() / 2, WIN_HEIGHT * 5 / 10 - texte.get_height() / 2))


# ----------------------------------------------------------------------------------------------------------------------
# Fenêtre
# ----------------------------------------------------------------------------------------------------------------------


def dessiner_fenetre_jeu(surface):
    """
    :param surface:
    :return: None
    """
    pygame.draw.rect(surface, COULEUR_FOND, (0, 0, WIN_GAME_WIDTH + WIN_BORDER * 2, WIN_GAME_HEIGHT + WIN_BORDER * 2))
    pygame.draw.rect(surface, COULEUR_BORDURE, (WIN_BORDER_GAP, WIN_BORDER_GAP, WIN_GAME_WIDTH + WIN_BORDER_WIDTH * 2, WIN_GAME_HEIGHT + WIN_BORDER_WIDTH * 2))
    pygame.draw.rect(surface, COULEUR_FOND, (WIN_BORDER, WIN_BORDER, WIN_GAME_WIDTH, WIN_GAME_HEIGHT))


# ----------------------------------------------------------------------------------------------------------------------
# Affichage
# ----------------------------------------------------------------------------------------------------------------------


def afficher(surface, data, coord):
    """
    :param surface:
    :param data:
    :param coord:
    :return: None
    """
    surface.blit(data, coord)


# ----------------------------------------------------------------------------------------------------------------------
# Chargement
# ----------------------------------------------------------------------------------------------------------------------


def charger_image(chemin, surface):
    """
    :param chemin:
    :param surface:
    :return: image
    """
    return pygame.image.load(chemin).convert_alpha(surface)


def charger_images_tetes(snake, surface):
    """
    :param snake:
    :param surface:
    :return: snake
    """
    img_tete_haut = charger_image(CHEMIN_TETE_HAUT, surface)
    img_tete_bas = charger_image(CHEMIN_TETE_BAS, surface)
    img_tete_gauche = charger_image(CHEMIN_TETE_GAUCHE, surface)
    img_tete_droite = charger_image(CHEMIN_TETE_DROITE, surface)
    snake["images"] = {"haut": img_tete_haut, "bas": img_tete_bas, "gauche": img_tete_gauche, "droite": img_tete_droite}


# ----------------------------------------------------------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------------------------------------------------------


def dessiner_menu_debut(surface):
    """
    :param surface:
    :return: dict{str: dict{"etat": bool, "coord": tuple(int, int), "hauteur": int, "largeur": int, "valeur": int}}
    """
    # Variable
    liste_menu = []
    # Dessiner menu début
    surface.fill(COULEUR_FOND)
    texte_police = pygame.font.Font(None, 60)
    texte_titre = texte_police.render("SNAKE", True, COULEUR_SNAKE)
    texte_titre_coord = (WIN_WIDTH // 2 - texte_titre.get_width() // 2, 1 / 6 * WIN_HEIGHT - texte_titre.get_height() // 2)
    afficher(surface, texte_titre, texte_titre_coord)
    texte_police = pygame.font.Font(None, 40)
    texte_jouer = texte_police.render("Jouer", True, COULEUR_TEXTE)
    texte_jouer_coord = (WIN_WIDTH // 2 - texte_jouer.get_width() // 2, 3 / 6 * WIN_HEIGHT - texte_jouer.get_height() // 2)
    afficher(surface, texte_jouer, texte_jouer_coord)
    ajouter_choix_menu(liste_menu, texte_jouer, texte_jouer_coord, 1)
    texte_quitter = texte_police.render("Quitter", True, COULEUR_TEXTE)
    texte_quitter_coord = (WIN_WIDTH // 2 - texte_quitter.get_width() // 2, 4 / 6 * WIN_HEIGHT - texte_quitter.get_height() // 2)
    afficher(surface, texte_quitter, texte_quitter_coord)
    ajouter_choix_menu(liste_menu, texte_quitter, texte_quitter_coord, 0)
    pygame.display.update()
    return liste_menu


def dessiner_menu_fin(surface, etat):
    """
    :param surface:
    :param etat: True -> gagné | False -> perdu
    :return: dict{str: dict{"etat": bool, "coord": tuple(int, int), "hauteur": int, "largeur": int, "valeur": int}}
    """
    # Variable
    liste_menu = []
    # Dessiner menu fin
    texte_police = pygame.font.Font(None, 60)
    if etat:
        texte_fin = texte_police.render("Bravo", True, COULEUR_BORDURE)
    else:
        texte_fin = texte_police.render("Aïe", True, COULEUR_BORDURE)
    afficher(surface, texte_fin, ((WIN_GAME_WIDTH + 2 * WIN_BORDER) // 2 - texte_fin.get_width() // 2, WIN_HEIGHT * 1 / 6 - texte_fin.get_height() // 2))
    texte_police = pygame.font.Font(None, 40)
    texte_rejouer = texte_police.render("Rejouer", True, COULEUR_TEXTE)
    texte_rejouer_coord = ((WIN_GAME_WIDTH + 2 * WIN_BORDER) // 2 - texte_rejouer.get_width() // 2, 3 / 6 * WIN_HEIGHT - texte_rejouer.get_height() // 2)
    afficher(surface, texte_rejouer, texte_rejouer_coord)
    ajouter_choix_menu(liste_menu, texte_rejouer, texte_rejouer_coord, 1)
    texte_quitter = texte_police.render("Quitter", True, COULEUR_TEXTE)
    texte_quitter_coord = ((WIN_GAME_WIDTH + 2 * WIN_BORDER) // 2 - texte_quitter.get_width() // 2, 4 / 6 * WIN_HEIGHT - texte_quitter.get_height() // 2)
    afficher(surface, texte_quitter, texte_quitter_coord)
    ajouter_choix_menu(liste_menu, texte_quitter, texte_quitter_coord, 0)
    pygame.display.update()
    return liste_menu


def dessiner_contour(surface, choix, couleur):
    """
    :param surface:
    :param choix:
    :param couleur:
    :return: None
    """
    pygame.draw.polygon(surface, couleur, [(choix["coord"][0] - CADRE_GAP, choix["coord"][1] - CADRE_GAP), (choix["coord"][0] + choix["largeur"] + CADRE_GAP, choix["coord"][1] - CADRE_GAP), (choix["coord"][0] + choix["largeur"] + CADRE_GAP, choix["coord"][1] + choix["hauteur"] + CADRE_GAP), (choix["coord"][0] - CADRE_GAP, choix["coord"][1] + choix["hauteur"] + CADRE_GAP)], CADRE_WIDTH)
    pygame.display.update()


def ajouter_choix_menu(liste_menu, texte, coord, valeur):
    """
    Ajoute un choix à la liste du menu
    :param liste_menu:
    :param texte:
    :param coord:
    :param valeur:
    :return: None
    """
    liste_menu.append({"etat": False, "coord": coord, "hauteur": texte.get_height(), "largeur": texte.get_width(), "valeur": valeur})

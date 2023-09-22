# ######################################################################################################################
# IMPORTATIONS
# ######################################################################################################################


from functions import *
from save import *


# ######################################################################################################################
# FONCTIONS
# ######################################################################################################################


def init():
    """
    Initialise le snake
    :return: dict{"corps": list[dict{"x": int, "y": int, "direction": droite}], "direction_future": str, "compteur": int, "pomme": int, "pomme_attente": int}
    """
    corps = [{"x": BOX_WIDTH // 2 * BOX_SIZE - i * BOX_SIZE + WIN_BORDER, "y": BOX_HEIGHT // 2 * BOX_SIZE + WIN_BORDER, "direction": "droite"} for i in range(SNAKE_SIZE, -1, -1)]
    snake = {"corps": corps, "direction_future": "droite", "compteur": 0, "pomme": 0, "pomme_attente": 0}
    return snake


def play(surface, snake):
    """
    :param surface:
    :param snake:
    :return: None
    """

    # Chargement des fichiers externes
    charger_images_tetes(snake, surface)
    image_pomme_petite = charger_image(CHEMIN_POMME, surface)
    image_pomme_grande = charger_image(CHEMIN_POMME_GRANDE, surface)

    # Mise en page de la fenêtre
    # - Fenêtre de jeu
    dessiner_fenetre_jeu(surface)
    dessiner_snake(snake, surface)
    pomme_coord = nouvelle_pomme(snake)
    afficher(surface, image_pomme_petite, pomme_coord)
    pygame.draw.rect(surface, COULEUR_WIN_TEXT, (WIN_WIDTH - WIN_TEXT, 0, WIN_TEXT, WIN_HEIGHT))
    # - Fenêtre text
    texte_police = pygame.font.Font(None, 40)
    texte_record = texte_police.render("Record", True, COULEUR_TEXTE, COULEUR_WIN_TEXT)
    afficher(surface, texte_record, (WIN_WIDTH - WIN_TEXT / 2 - texte_record.get_width() / 2, WIN_HEIGHT * 1 / 10 - texte_record.get_height() / 2))
    texte_record_nombre = texte_police.render(recuperer_fichier(FICHIER_SAUVEGARDE)["record"], True, COULEUR_TEXTE, COULEUR_WIN_TEXT)
    afficher(surface, texte_record_nombre, (WIN_WIDTH - WIN_TEXT / 2 - texte_record_nombre.get_width() / 2, WIN_HEIGHT * 2 / 10 - texte_record_nombre.get_height() / 2))
    afficher(surface, image_pomme_grande, (WIN_WIDTH - WIN_TEXT / 2 - image_pomme_grande.get_width() / 2, WIN_HEIGHT * 4 / 10 - image_pomme_grande.get_height() / 2))
    ecrire_texte_pomme(snake, texte_police, surface)
    # - Actualisation de la fenêtre
    pygame.display.update()

    # Horloge
    horloge = pygame.time.Clock()

    # Initialisation de la variable de jeu
    game = 1  # 0 -> arrêt | 1 -> en cours | 2 -> perdu | 3 -> gagné

    # Départ
    depart = False
    texte_police = pygame.font.Font(None, 25)
    texte_aide = texte_police.render("Appuyez sur 'SPACE' pour commencer !", True, COULEUR_BLANC)
    texte_aide_coord = ((WIN_GAME_WIDTH + WIN_BORDER * 2) // 2 - texte_aide.get_width() // 2, WIN_HEIGHT // 1 / 5 - texte_aide.get_height() // 2)
    compteur = 0
    while not depart:

        # Images par seconde
        horloge.tick(FPS_DEPART)

        # Boucle des événements
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                game = 0
                depart = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    depart = True

        # Actualisation des variables
        compteur += 1
        if compteur > FPS_DEPART:
            compteur = 0

        # Affichage de l'aide
        if compteur == FPS_DEPART // 2:
            afficher(surface, texte_aide, texte_aide_coord)
        if compteur == 0:
            pygame.draw.rect(surface, COULEUR_FOND, (texte_aide_coord[0], texte_aide_coord[1], texte_aide.get_width(), texte_aide.get_height()))
            afficher(surface, image_pomme_petite, pomme_coord)

        # Actualisation de la fenêtre
        pygame.display.update()

    # Initialisation de la police
    texte_police = pygame.font.Font(None, 40)

    # Boucle de jeu
    while game == 1:

        # Images par seconde
        horloge.tick(FPS)

        # Boucle des événements
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                game = 0
            if event.type == pygame.KEYDOWN:
                if (event.key in [pygame.K_UP, pygame.K_z]) and snake["corps"][-1]["direction"] != "bas":
                    snake["direction_future"] = "haut"
                if (event.key in [pygame.K_DOWN, pygame.K_s]) and snake["corps"][-1]["direction"] != "haut":
                    snake["direction_future"] = "bas"
                if (event.key in [pygame.K_LEFT, pygame.K_q]) and snake["corps"][-1]["direction"] != "droite":
                    snake["direction_future"] = "gauche"
                if (event.key in [pygame.K_RIGHT, pygame.K_d]) and snake["corps"][-1]["direction"] != "gauche":
                    snake["direction_future"] = "droite"

        # Déplacement du serpent
        snake["compteur"] += 1
        if snake["compteur"] > BOX_WIDTH:
            snake["compteur"] = 0

            # - Travail sur le "corps" du serpent
            del snake["corps"][0]
            if snake["direction_future"] == "haut":
                if (snake["corps"][-1]["y"] - BOX_SIZE < WIN_BORDER) or \
                        ((snake["corps"][-1]["x"], snake["corps"][-1]["y"] - BOX_SIZE) in [(partie["x"], partie["y"]) for partie in snake["corps"]]):
                    game = 2
                snake["corps"].append({"x": snake["corps"][-1]["x"], "y": snake["corps"][-1]["y"] - BOX_SIZE, "direction": snake["direction_future"]})
            elif snake["direction_future"] == "bas":
                if (snake["corps"][-1]["y"] + BOX_SIZE >= WIN_GAME_HEIGHT + WIN_BORDER) or \
                        ((snake["corps"][-1]["x"], snake["corps"][-1]["y"] + BOX_SIZE) in [(partie["x"], partie["y"]) for partie in snake["corps"]]):
                    game = 2
                snake["corps"].append({"x": snake["corps"][-1]["x"], "y": snake["corps"][-1]["y"] + BOX_SIZE, "direction": snake["direction_future"]})
            elif snake["direction_future"] == "gauche":
                if (snake["corps"][-1]["x"] - BOX_SIZE < WIN_BORDER) or \
                        ((snake["corps"][-1]["x"] - BOX_SIZE, snake["corps"][-1]["y"]) in [(partie["x"], partie["y"]) for partie in snake["corps"]]):
                    game = 2
                snake["corps"].append({"x": snake["corps"][-1]["x"] - BOX_SIZE, "y": snake["corps"][-1]["y"], "direction": snake["direction_future"]})
            elif snake["direction_future"] == "droite":
                if (snake["corps"][-1]["x"] + BOX_SIZE >= WIN_GAME_WIDTH + WIN_BORDER) or \
                        ((snake["corps"][-1]["x"] + BOX_SIZE, snake["corps"][-1]["y"]) in [(partie["x"], partie["y"]) for partie in snake["corps"]]):
                    game = 2
                snake["corps"].append({"x": snake["corps"][-1]["x"] + BOX_SIZE, "y": snake["corps"][-1]["y"], "direction": snake["direction_future"]})

            # - Dessiner la fenêtre de jeu
            dessiner_fenetre_jeu(surface)

            # - Pomme
            if (snake["corps"][-1]["x"], snake["corps"][-1]["y"]) == pomme_coord:
                snake["pomme"] += 1
                snake["pomme_attente"] += 1
                ecrire_texte_pomme(snake, texte_police, surface)
                snake["corps"].insert(0, snake["corps"][0])
                if snake["pomme"] == POMME_MAX:
                    game = 3
                    snake["compteur"] = BOX_WIDTH
                else:
                    pomme_coord = nouvelle_pomme(snake)

            # - Dessiner pomme
            afficher(surface, image_pomme_petite, pomme_coord)

        # - Dessiner le serpent
        dessiner_snake(snake, surface)

        # Actualisation de la fenêtre
        pygame.display.update()

    # Record
    if snake["pomme"] > int(recuperer_fichier(FICHIER_SAUVEGARDE)["record"]):
        ecrire_fichier({"record": snake["pomme"]}, FICHIER_SAUVEGARDE)

    return game

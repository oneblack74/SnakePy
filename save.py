def recuperer_fichier(fichier):
    """
    :param fichier:
    :return: dict{key: val}
    """
    data = {}
    sauvegarde = open(fichier, "r")
    for ligne in sauvegarde:
        cle, valeur = ligne[:-1].split(" : ")  # [:-1] permet de ne pas prendre en compte les sauts de ligne (\n)
        data[cle] = valeur
    sauvegarde.close()
    return data


def ecrire_fichier(data, fichier):
    """
    :param data: dict{key: val}
    :param fichier:
    :return: None
    """
    sauvegarde = open(fichier, "w")
    for cle, valeur in data.items():
        sauvegarde.write(str(cle) + " : " + str(valeur) + "\n")
    sauvegarde.close()

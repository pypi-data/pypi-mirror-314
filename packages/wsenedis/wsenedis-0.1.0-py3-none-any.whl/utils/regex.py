import re


def verification_prm(id):
    if len(id) == 0 or re.fullmatch(r"[0-9]{14}", id) == None:
        raise ValueError('le champ point_id doit être une chaine de 14 caractères numériques')
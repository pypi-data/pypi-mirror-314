from __future__ import annotations


class PersonnePhysique(dict):
    def __init__(self, nom: str, civilite: str = None, prenom: str = None):
        _kwargs = {'nom': nom}
        if civilite is not None:
            _kwargs['civilite'] = civilite
        if prenom is not None:
            _kwargs['prenom'] = prenom
        dict.__init__(self, **_kwargs)


class PersonneMorale(dict):
    def __init__(self, denomination_sociale: str):
        _kwargs = {'denominationSociale': denomination_sociale}
        dict.__init__(self, **_kwargs)


class DeclarationAccordClient(dict):
    def __init__(self, personne_physique_ou_morale: PersonnePhysique | PersonneMorale, accord=False):
        _kwargs = {'accord': accord}
        if isinstance(personne_physique_ou_morale, PersonnePhysique):
            _kwargs['personnePhysique'] = personne_physique_ou_morale
        elif isinstance(personne_physique_ou_morale, PersonneMorale):
            _kwargs['personneMorale'] = personne_physique_ou_morale
        else:
            raise ValueError('un objet de type PersonnePhysique ou PersonneMorale est attendu en premier argument')
        dict.__init__(self, **_kwargs)
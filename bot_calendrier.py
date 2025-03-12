def get_lumharel_date():
    """ 📆 Calcule la date dans le calendrier de Lumharel """
    date_actuelle = datetime.date.today()
    jours_ecoules = (date_actuelle - date_reference).days  

    # 🔄 Calcul des jours, mois et années
    jour_semaine_index = (jours_ecoules + 6) % 8  
    jour_semaine = jours_complet[jour_semaine_index]

    jours_depuis_ref = jours_ecoules
    mois_nom = lumharel_reference["mois"]
    jour_mois = lumharel_reference["jour"]

    while jours_depuis_ref > 0:
        duree_mois = mois_durees[mois_nom]
        if mois_nom == "Eldros" and (date_actuelle.year - date_reference.year) % 2 == 0:
            duree_mois += 1  

        if jour_mois + jours_depuis_ref <= duree_mois:
            jour_mois += jours_depuis_ref
            jours_depuis_ref = 0
        else:
            jours_depuis_ref -= (duree_mois - jour_mois + 1)
            mois_nom = mois_noms[(mois_noms.index(mois_nom) + 1) % len(mois_noms)]
            jour_mois = 1

    # 🌙 **Correction des phases lunaires**
    phase_astraelis = phases_lunaires[(jours_ecoules % jours_cycle_astraelis) // 4]
    phase_vorna = phases_lunaires_vorna[(jours_ecoules % jours_cycle_vorna) // 6]

    festivite_du_jour = festivites.get((jour_mois, mois_nom), "Aucune")

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

import os
import discord
from discord.ext import tasks, commands
import datetime
import random
import pytz

from zoneinfo import ZoneInfo

# Fuseau horaire Europe/Paris pour éviter le décalage UTC de Railway
TZ = ZoneInfo("Europe/Paris")

def now_paris():
    return datetime.datetime.now(TZ)

def today_paris():
    return now_paris().date()
    
# Vérification de l'heure système
print(f"🕒 [DEBUG] Heure système Railway : {datetime.datetime.now()}")

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1348851808549867602  

POST_HOUR = 10
POST_MINUTE = 30

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Jours et mois de Lumharel
jours_complet = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvael", "Luméon", "Kaelios", "Eldrith"]
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]

mois_durees = {
    "Orréa": 32, "Thiloris": 28, "Vækirn": 32, "Dornis": 32, "Solvannar": 32,
    "Velkaris": 28, "Nytheris": 32, "Varneth": 28, "Elthiris": 32, "Zorvahl": 32,
    "Draknar": 28, "Umbraël": 32, "Aëldrin": 32, "Kaelthor": 28, "Eldros": 32
}
mois_noms = list(mois_durees.keys())

# Phases lunaires (cycle basé sur le 12 mars 2025 comme référence)
phases_lune = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
cycle_astraelis = 32  
cycle_vorna = 48  

# Références pour la correspondance des dates et des phases lunaires
ref_date_irl = datetime.date(2025, 3, 12)  
ref_date_lumharel = (7, "Vækirn", 1532)  
ref_phase_astraelis = 4  # 🌕 Full Moon pour Astrealis le 12 mars 2025
ref_phase_vorna = 0  # 🌑 New Moon pour Vörna le 12 mars 2025

# Messages immersifs
messages_accueil = [
    "✨ Que les vents de Lumharel vous soient favorables !",
    "🌙 Que la lumière des lunes vous guide en cette journée !",
    "🔥 Puisse la flamme de Vaek illuminer votre chemin !",
    "🌿 Que les murmures des anciens Façonneurs vous inspirent aujourd’hui !"
]

# Festivités fixes
festivites = [
    ((1, "Orréa"), (3, "Orréa"), "Solstice du Grand Réveil"),
    ((19, "Orréa"), (19, "Orréa"), "Fête des Pattes Mouillées"),
    ((28, "Thiloris"), (28, "Thiloris"), "Sillons Chuchotants"),
    ((15, "Vækirn"), (17, "Vækirn"), "Festival des Flammes"),
    ((9, "Dornis"), (9, "Dornis"), "Cendres Joyeuses"),
    ((21, "Dornis"), (21, "Dornis"), "Jeux de la Flamme Tournante"),
    ((16, "Umbraël"), (16, "Umbraël"), "Nuit de la Lune Noire"),
    ((31, "Nytheris"), (1, "Varneth"), "Nuit des Légendes"),
    ((8, "Varneth"), (8, "Varneth"), "Bal des Errants"),
    ((17, "Elthiris"), (17, "Elthiris"), "Festival des Rouleaux Volants"),
    ((3, "Draknar"), (6, "Draknar"), "Veillée des Ombres"),
    ((12, "Umbraël"), (12, "Umbraël"), "Nuit des Mille Lueurs"),
    ((18, "Umbraël"), (18, "Umbraël"), "Fête des Échos Perdus"),
    ((7, "Kaelthor"), (10, "Kaelthor"), "Grande Récitation"),
    ((15, "Kaelthor"), (15, "Kaelthor"), "Jour des Fragments de Rêves"),
    ((26, "Eldros"), (26, "Eldros"), "Chant du Dernier Souffle")
]
def get_festivite_du_jour(jour, mois):
    for (start_day, start_month), (end_day, end_month), nom in festivites:
        if start_month == end_month:
            if mois == start_month and start_day <= jour <= end_day:
                return nom
        else:
            if (mois == start_month and jour >= start_day) or (mois == end_month and jour <= end_day):
                return nom
    return "Aucune"
    
### 🔹 **Convertir la date IRL en date Lumharel**
def get_lumharel_date():
    """ Calcule la date en Lumharel à partir de la date IRL du 12 mars 2025 comme référence. """
    date_actuelle = today_paris()
    delta_jours = (date_actuelle - ref_date_irl).days  

    jours_ecoules = ref_date_lumharel[0] - 1  
    mois_nom = ref_date_lumharel[1]
    annee = ref_date_lumharel[2]
    mois_index = mois_noms.index(mois_nom)

    while delta_jours > 0:
        jours_restants = mois_durees[mois_noms[mois_index]] - jours_ecoules
        if delta_jours >= jours_restants:
            delta_jours -= jours_restants
            mois_index = (mois_index + 1) % len(mois_noms)
            jours_ecoules = 0
            if mois_index == 0:
                annee += 1  
        else:
            jours_ecoules += delta_jours
            delta_jours = 0

    jour_mois = jours_ecoules + 1
    mois_nom = mois_noms[mois_index]

    # ✅ Corrigé : on prend tous les jours écoulés depuis 7 Vækirn
    index_ref = 2  # 12 mars 2025 = Vaeldris
    delta_jours = (date_actuelle - ref_date_irl).days
    jour_semaine = jours_complet[(index_ref + delta_jours) % 8]

    # 🔹 **Calcul des phases lunaires corrigé**
    jours_depuis_ref = (date_actuelle - ref_date_irl).days

    # Astrealis (cycle de 32 jours, 8 phases de 4 jours chacune)
    phase_astraelis_index = (ref_phase_astraelis + (jours_depuis_ref // 4)) % 8
    phase_astraelis = phases_lune[phase_astraelis_index]

    # Vörna (cycle de 48 jours, 8 phases de 6 jours chacune)
    phase_vorna_index = (ref_phase_vorna + (jours_depuis_ref // 6)) % 8
    phase_vorna = phases_lune[phase_vorna_index]

    festivite_du_jour = get_festivite_du_jour(jour_mois, mois_nom)

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

def generate_calendar(mois_nom, jour_mois):
    calendrier = "\n\n"
    cell_width = 6
    nb_colonnes = len(jours_abbr)

    # En-tête des jours
    calendrier += "".join([f"{abbr:^{cell_width}}" for abbr in jours_abbr]) + "\n"
    calendrier += "-" * (cell_width * nb_colonnes) + "\n"

    nb_jours = mois_durees[mois_nom]

    # Calcul du jour de la semaine du 1er jour du mois
    date_actuelle = today_paris()
    total_jours_irl = (date_actuelle - ref_date_irl).days
    jours_ecoules_depuis_ref = total_jours_irl + (ref_date_lumharel[0] - 1)

    jours_depuis_debut = 0
    current_index = mois_noms.index(ref_date_lumharel[1])
    current_jour = ref_date_lumharel[0] - 1
    jours_restants = jours_ecoules_depuis_ref

    while jours_restants > 0:
        reste_mois = mois_durees[mois_noms[current_index]] - current_jour
        if jours_restants >= reste_mois:
            jours_restants -= reste_mois
            jours_depuis_debut += reste_mois
            current_index = (current_index + 1) % len(mois_noms)
            current_jour = 0
        else:
            jours_depuis_debut += jours_restants
            jours_restants = 0

    index_ref = 2  # 12 mars 2025 = Vaeldris
    jours_depuis_ref = (date_actuelle - ref_date_irl).days
    jours_recul = jour_mois - 1  # On recule au 1er du mois
    premier_jour_index = (index_ref + (jours_depuis_ref - jours_recul)) % 8

    ligne = " " * (cell_width * premier_jour_index)
    jour_semaine_index = premier_jour_index

    for i in range(1, nb_jours + 1):
        if i == jour_mois:
            ligne += f"[{i:2}]".center(cell_width)
        else:
            ligne += f" {i:2} ".center(cell_width)

        jour_semaine_index = (jour_semaine_index + 1) % 8

        if jour_semaine_index == 0:
            calendrier += ligne.rstrip() + "\n"
            ligne = ""

    if ligne:
        calendrier += ligne.rstrip() + "\n"

    return calendrier

### 🔹 **Message du calendrier**
async def send_calendar_message(channel):
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    message_immersion = random.choice(messages_accueil)
    calendrier_formatte = generate_calendar(mois, jour_mois)

        # Détection du Marché des Lunes (nouvelle OU pleine double)
    if (phase_astraelis == "🌑" and phase_vorna == "🌑") or (phase_astraelis == "🌕" and phase_vorna == "🌕"):
        if festivite == "Aucune":
            festivite = "Marché des Lunes"
        else:
            festivite += " & Marché des Lunes"

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1533 - Ère du Cycle Unifié**\n\n"
                    f"📆 *Correspondance IRL : {date_reelle.strftime('%d/%m/%Y')}*\n\n"
                    f"{message_immersion}",
        color=0xFFD700
    )

    embed.add_field(name="🎉 Festivité", value=f"**{festivite}**", inline=True)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astrealis : {phase_astraelis} | Vörna : {phase_vorna}", inline=True)
    embed.add_field(name="🗓️ Mois en cours", value=f"```\n{calendrier_formatte}\n```", inline=False)
    embed.add_field(name="🔗 Calendrier complet", value="[Voir en ligne](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    await channel.send(embed=embed)


@bot.command(name="calendrier")
async def calendrier(ctx):
    """Affiche la date et le calendrier en temps réel"""
    await send_calendar_message(ctx.channel)

@bot.command(name="test")
async def test(ctx):
    await ctx.send("✅ Le bot a bien reçu la commande !")
    print(f"[DEBUG] Test reçu de {ctx.author}")

@bot.command(name="debugcalendrier")
async def debug_calendrier(ctx):
    """ Affiche les détails bruts de la conversion de date pour débogage """
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    
    await ctx.send(
        f"📅 **DEBUG CALENDRIER**\n\n"
        f"🗓️ Date IRL : {date_reelle.strftime('%A %d %B %Y')}\n"
        f"📜 Date IG : {jour_mois} {mois} ({jour_semaine}), 1532\n"
        f"🌙 Phases lunaires : Astrealis {phase_astraelis} | Vörna {phase_vorna}\n"
        f"🎉 Festivité du jour : {festivite}"
    )

@tasks.loop(seconds=60)
async def send_daily_calendar():
    now = now_paris()
    if now.hour == POST_HOUR and now.minute == POST_MINUTE:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await send_calendar_message(channel)
            print(f"✅ [DEBUG] Calendrier envoyé automatiquement à {POST_HOUR:02d}h{POST_MINUTE:02d}.")
        else:
            print("❌ [ERROR] Channel non trouvé pour l'envoi automatique.")

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")

    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
    
    print(f"⏰ [DEBUG] Boucle d'envoi automatique lancée.")

if __name__ == "__main__":
    bot.run(TOKEN)




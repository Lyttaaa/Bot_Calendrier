import os
import discord
from discord.ext import tasks, commands
import datetime
import random
import pytz

# 🔥 Configuration du bot
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1348851808549867602

POST_HOUR = 10  # Heure d'envoi du message
POST_MINUTE = 30

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 📅 Jours & Mois de Lumharel
jours_complet = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvael", "Luméon", "Kaelios", "Eldrith"]
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois_noms = ["Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar", "Velkaris", "Nytheris", "Varneth", "Elthiris", "Zorvahl", "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"]
mois_durees = {
    "Orréa": 32, "Thiloris": 28, "Vækirn": 32, "Dornis": 32, "Solvannar": 32,
    "Velkaris": 28, "Nytheris": 32, "Varneth": 28, "Elthiris": 32, "Zorvahl": 32,
    "Draknar": 28, "Umbraël": 32, "Aëldrin": 32, "Kaelthor": 28, "Eldros": 32
}

# 🌙 Phases Lunaires (8 phases)
phases_lune = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]

# 📌 Référence de départ
date_reference = datetime.date(2025, 3, 12)  # Date IRL de référence
lumharel_reference = {"mois": "Vækirn", "jour": 7}  # Date dans Lumharel

# 🎉 Festivités
festivites = {
    (1, "Orréa"): "Solstice du Grand Réveil",
    (15, "Vækirn"): "Festival des Flammes",
    (32, "Umbraël"): "Nuit de la Lune Noire",
    (16, "Nytheris"): "Équinox des Vents",
    (28, "Thiloris"): "Nuit des Premiers Feux",
    (20, "Zorvahl"): "Veillée des Ombres",
    (32, "Elthiris"): "Nuit des Légendes",
    (1, "Aëldrin"): "Grande Récitation"
}

# 📅 Calcul de la Date & des Phases Lunaires
def get_lumharel_date():
    """ Calcule la date et les phases lunaires """
    date_actuelle = datetime.date.today()
    jours_ecoules = (date_actuelle - date_reference).days

    # 🔹 Jour de la semaine
    jour_semaine_index = (jours_ecoules + 6) % 8
    jour_semaine = jours_complet[jour_semaine_index]

    # 🔹 Calcul du mois et du jour
    jours_depuis_ref = jours_ecoules
    mois_nom = lumharel_reference["mois"]
    jour_mois = lumharel_reference["jour"]

    while jours_depuis_ref > 0:
        duree_mois = mois_durees[mois_nom]
        if mois_nom == "Eldros" and (date_actuelle.year - date_reference.year) % 2 == 0:
            duree_mois += 1  # Ajout du 33e jour tous les 2 ans

        if jour_mois + jours_depuis_ref <= duree_mois:
            jour_mois += jours_depuis_ref
            jours_depuis_ref = 0
        else:
            jours_depuis_ref -= (duree_mois - jour_mois + 1)
            mois_nom = mois_noms[(mois_noms.index(mois_nom) + 1) % len(mois_noms)]
            jour_mois = 1

    # 🌙 **Calcul des phases lunaires avec précision**
    phase_astraelis = phases_lune[(jours_ecoules % 32) // 4]  # 1 phase = 4 jours
    phase_vorna = phases_lune[(jours_ecoules % 48) // 6]  # 1 phase = 6 jours

    festivite_du_jour = festivites.get((jour_mois, mois_nom), "Aucune")

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

# 🗓️ Génération du calendrier formaté
def generate_calendar(mois_nom, jour_mois):
    """ Génère le calendrier en tableau """
    nb_jours = mois_durees[mois_nom]
    calendrier = "\n\n"

    # En-tête
    calendrier += "   ".join([f"{abbr:^4}" for abbr in jours_abbr]) + "\n"
    calendrier += "-" * 48 + "\n"

    # Générer les jours du mois
    ligne = ""
    for i in range(1, nb_jours + 1):
        if i == jour_mois:
            ligne += f"[{i:2}]   "  # Mettre le jour actuel entre []
        else:
            ligne += f" {i:2}    "

        # Retour à la ligne après chaque semaine de 8 jours
        if i % 8 == 0:
            calendrier += ligne.rstrip() + "\n"
            ligne = ""

    return calendrier

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()

@tasks.loop(seconds=60)
async def send_daily_calendar():
    now = datetime.datetime.now()
    if now.hour == POST_HOUR and now.minute == POST_MINUTE:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await send_calendar_message(channel)

async def send_calendar_message(channel):
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    calendrier_formatte = generate_calendar(mois, jour_mois)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n"
                    f"📆 *Correspondance réelle : {date_reelle.strftime('%d/%m/%Y')}*",
        color=0xFFD700
    )
    embed.add_field(name="🎉 Festivité du jour", value=f"**{festivite}**", inline=True)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astrealis : {phase_astraelis}\nVörna : {phase_vorna}", inline=True)
    embed.add_field(name="🗓️ Mois en cours", value=f"```\n{calendrier_formatte}\n```", inline=False)
    embed.add_field(name="📅 Voir le calendrier complet", value="[🔗 Cliquez ici](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    await channel.send(embed=embed)

@bot.command(name="calendrier")
async def calendrier(ctx):
    await send_calendar_message(ctx.channel)

bot.run(TOKEN)

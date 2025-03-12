import os
import discord
from discord.ext import tasks, commands
import datetime
import random
import pytz

TOKEN = os.getenv("TOKEN")  
CHANNEL_ID = 1348851808549867602  

POST_HOUR = 10  
POST_MINUTE = 30  

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Jours et mois du calendrier de Lumharel
jours_complet = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvaël", "Luméon", "Kaelios", "Eldrith"]
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois_noms = [
    "Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar", "Velkaris", "Nytheris",
    "Varneth", "Elthiris", "Zorvahl", "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"
]
mois_durees = {
    "Orréa": 32, "Thiloris": 28, "Vækirn": 32, "Dornis": 32, "Solvannar": 32,
    "Velkaris": 28, "Nytheris": 32, "Varneth": 28, "Elthiris": 32, "Zorvahl": 32,
    "Draknar": 28, "Umbraël": 32, "Aëldrin": 32, "Kaelthor": 28, "Eldros": 32
}

def is_bissextile(year):
    return year % 2 == 0

# Point de départ du calendrier : 1er Tellion d'Orréa 1532 correspond au 1er mars 2025
date_reference = datetime.date(2025, 3, 1)  
jours_cycle_astraelis = 32
jours_cycle_vorna = 48
phases_lunaires = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]

# Messages immersifs
messages_accueil = [
    "✨ Que les vents de Lumharel vous soient favorables !",
    "🌙 Que la lumière des lunes vous guide en cette journée !",
    "🔥 Puisse la flamme de Vaek illuminer votre chemin !",
    "🌿 Que les murmures des anciens Façonneurs vous inspirent aujourd’hui !"
]

# Liste des festivités fixes
festivites = {
    (1, "Orréa"): "Solstice du Grand Réveil",
    (15, "Vækirn"): "Festival des Flammes",
    (32, "Umbraël"): "Nuit de la Lune Noire",
    (16, "Nytheris"): "Équinox des Vents",
    (28, "Thiloris"): "Nuit des Premiers Feux",
    (20, "Zorvahl"): "Veillée des Ombres",
    (32, "Elthiris"): "Nuit des Légendes",
    (1, "Aëldrin"): "Grande Récitation",
    (33, "Eldros"): "Jour du Souffle Perdu (tous les 2 ans)"
}

def get_lumharel_date():
    """ Calcule la date actuelle dans le calendrier de Lumharel """
    date_actuelle = datetime.date.today()
    jours_ecoules = (date_actuelle - date_reference).days  

    mois_nom = None
    jour_mois = None
    jour_compte = jours_ecoules

    for mois, duree in mois_durees.items():
        if mois == "Eldros" and is_bissextile(date_actuelle.year):
            duree += 1  

        if jour_compte <= duree:
            mois_nom = mois
            jour_mois = jour_compte
            break
        jour_compte -= duree

    if mois_nom is None or jour_mois is None:
        mois_nom = "Orréa"
        jour_mois = 1

    jour_semaine_index = (jours_ecoules - 1) % 8
    jour_semaine = jours_complet[jour_semaine_index]

    jours_depuis_ref = (date_actuelle - date_reference).days
    phase_astraelis = phases_lunaires[(jours_depuis_ref % jours_cycle_astraelis) // 4]
    phase_vorna = phases_lunaires[(jours_depuis_ref % jours_cycle_vorna) // 6]

    festivite_du_jour = festivites.get((jour_mois, mois_nom), "Aucune")

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

def generate_calendar(mois_nom, jour_mois):
    """ Génère le tableau du calendrier """
    nb_jours = mois_durees.get(mois_nom, 32)
    calendrier = "\n\n"

    calendrier += "   ".join([f"{abbr:^4}" for abbr in jours_abbr]) + "\n"
    calendrier += "-" * 48 + "\n"

    ligne = ""
    for i in range(1, nb_jours + 1):
        if i == jour_mois:
            ligne += f"[{i:2}]   "  
        else:
            ligne += f" {i:2}    "

        if i % 8 == 0:
            calendrier += ligne.rstrip() + "\n"
            ligne = ""

    return calendrier

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()

@bot.command(name="calendrier")
async def calendrier(ctx):
    """ Affiche la date et le calendrier en temps réel """
    await send_calendar_message(ctx.channel)

@tasks.loop(seconds=60)
async def send_daily_calendar():
    """ Vérifie l'heure chaque minute et envoie le calendrier si nécessaire """
    now_local = datetime.datetime.now(pytz.timezone("Europe/Paris"))

    if now_local.hour == POST_HOUR and now_local.minute == POST_MINUTE:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await send_calendar_message(channel)

async def send_calendar_message(channel):
    """ Génère et envoie le message du calendrier """
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    message_immersion = random.choice(messages_accueil)
    calendrier_formatte = generate_calendar(mois, jour_mois)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n"
                    f"📆 *Correspondance dans notre monde : {date_reelle.strftime('%d/%m/%Y')}*\n\n"
                    f"{message_immersion}",
        color=0xFFD700
    )

    embed.add_field(name="🎉 Festivité du jour", value=f"**{festivite}**", inline=True)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astraelis : {phase_astraelis}\nVörna : {phase_vorna}", inline=True)
    embed.add_field(name="🗓️ Mois en cours", value=f"```\n{calendrier_formatte}\n```", inline=False)

    await channel.send(embed=embed)

bot.run(TOKEN)

import os
import discord
from discord.ext import tasks, commands
import datetime
import random

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1348851808549867602  # Remplace ce nombre par l'ID de ton canal Discord

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Définition des noms des jours et des mois
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois_noms = [
    "Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar",
    "Velkaris", "Nytheris", "Varneth", "Elthiris", "Zorvahl",
    "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"
]

# Définition des phases des lunes
phases_astraelis = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
phases_vorna = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]

# Message immersif
messages_accueil = [
    "✨ Que les vents de Lumharel vous soient favorables !",
    "🌙 Que la lumière des lunes vous guide en cette journée !",
    "🔥 Puisse la flamme de Vaek illuminer votre chemin !",
    "🌿 Que les murmures des anciens Façonneurs vous inspirent aujourd’hui !"
]

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")
    send_daily_calendar.start()

def get_lumharel_date():
    """ Calcule la date dans le calendrier de Lumharel """
    date_actuelle = datetime.date.today()
    jour_annee = date_actuelle.timetuple().tm_yday  # Jour de l'année (1 à 365/366)

    # Calcul du mois et du jour
    mois_index = (jour_annee - 1) // 32
    jour_mois = ((jour_annee - 1) % 32) + 1

    # Calcul du jour de la semaine
    jour_semaine_index = (jour_annee - 1) % 8
    jour_semaine = jours_abbr[jour_semaine_index]

    # Phase des lunes
    phase_astraelis = phases_astraelis[(jour_annee % len(phases_astraelis))]
    phase_vorna = phases_vorna[(jour_annee % len(phases_vorna))]

    return mois_noms[mois_index], jour_mois, jour_semaine, phase_astraelis, phase_vorna

def generer_calendrier(mois, jour_mois):
    """ Génère le calendrier du mois en cours avec le jour actuel en crochets """
    jours_mois = []
    for i in range(1, 33):
        jour_str = f"{i:2}"
        if i == jour_mois:
            jour_str = f"[{jour_str.strip()}]"
        jours_mois.append(jour_str)

    jours_abbr_str = "   ".join(jours_abbr)  # Alignement des jours
    ligne_separation = "─" * len(jours_abbr_str)

    calendrier_texte = f"{jours_abbr_str}\n{ligne_separation}\n"
    for i in range(0, len(jours_mois), 8):
        calendrier_texte += "   ".join(jours_mois[i:i+8]) + "\n"

    return calendrier_texte

@tasks.loop(hours=24)
async def send_daily_calendar():
    """ Envoie le calendrier chaque jour dans le canal """
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna = get_lumharel_date()
    calendrier = generer_calendrier(mois, jour_mois)
    message_immersion = random.choice(messages_accueil)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n{message_immersion}",
        color=0xFFD700
    )
    
    embed.add_field(name="📆 Mois en cours", value=f"```\n{calendrier}```", inline=False)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astraelis : {phase_astraelis} | Vörna : {phase_vorna}", inline=False)
    embed.add_field(name="📅 Lien vers le calendrier complet", value="[Voir le calendrier](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
    else:
        print("❌ Erreur : Channel introuvable ! Vérifie l'ID du canal.")

@bot.command(name="calendrier")
async def calendrier(ctx):
    """ Affiche la date actuelle dans le calendrier de Lumharel """
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna = get_lumharel_date()
    calendrier = generer_calendrier(mois, jour_mois)
    message_immersion = random.choice(messages_accueil)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n{message_immersion}",
        color=0xFFD700
    )
    
    embed.add_field(name="📆 Mois en cours", value=f"```\n{calendrier}```", inline=False)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astraelis : {phase_astraelis} | Vörna : {phase_vorna}", inline=False)
    embed.add_field(name="📅 Lien vers le calendrier complet", value="[Voir le calendrier](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="calendrierlien")
async def calendrier_lien(ctx):
    """ Envoie le lien vers le calendrier interactif """
    await ctx.send("📅 **Lien vers le calendrier du Cycle des Souffles** :\n🔗 https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78")

bot.run(TOKEN)

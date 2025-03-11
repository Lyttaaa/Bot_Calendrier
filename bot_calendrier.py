import os
import discord
from discord.ext import tasks, commands
import datetime
import random

TOKEN = os.getenv("TOKEN")  # Récupération du token depuis les variables d'environnement
CHANNEL_ID = 1348851808549867602  # Remplace avec l'ID de ton canal Discord

# 🔴 Définition de l'heure d'envoi du message
POST_HOUR = 12  # Heure en format 24h (ex: 8 = 08h00)
POST_MINUTE = 11  # Minute exacte (ex: 30 = 08h30)

intents = discord.Intents.default()
intents.message_content = True  # Ajoute cette ligne
bot = commands.Bot(command_prefix="!", intents=intents)

# Définition des noms des jours et des mois
jours_complet = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvael", "Luméon", "Kaelios", "Eldrith"]
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois_noms = [
    "Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar",
    "Velkaris", "Nytheris", "Varneth", "Elthiris", "Zorvahl",
    "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"
]

# Définition des phases des lunes
phases_astraelis = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
phases_vorna = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]

# Messages immersifs
messages_accueil = [
    "✨ Que les vents de Lumharel vous soient favorables !",
    "🌙 Que la lumière des lunes vous guide en cette journée !",
    "🔥 Puisse la flamme de Vaek illuminer votre chemin !",
    "🌿 Que les murmures des anciens Façonneurs vous inspirent aujourd’hui !"
]

# Liste dynamique des festivités
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

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()

def get_lumharel_date():
    """ Calcule la date dans le calendrier de Lumharel et les festivités associées """
    date_actuelle = datetime.date.today()
    jour_annee = date_actuelle.timetuple().tm_yday

    mois_index = (jour_annee - 1) // 32
    jour_mois = ((jour_annee - 1) % 32) + 1
    jour_semaine_index = (jour_annee - 1) % 8
    jour_semaine = jours_complet[jour_semaine_index]

    phase_astraelis = phases_astraelis[jour_annee % len(phases_astraelis)]
    phase_vorna = phases_vorna[jour_annee % len(phases_vorna)]

    mois_nom = mois_noms[mois_index]

    # Vérification des festivités fixes
    festivite_du_jour = festivites.get((jour_mois, mois_nom), "Aucune")

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

def generer_calendrier(mois, jour_mois):
    """ Génère le calendrier du mois en cours avec le jour actuel en crochets """
    jours_mois = []
    for i in range(1, 33):
        jour_str = f"{i:2}"
        if i == jour_mois:
            jour_str = f"[{jour_str.strip()}]"
        jours_mois.append(jour_str)

    jours_abbr_str = "  ".join(jours_abbr)
    ligne_separation = "─" * len(jours_abbr_str)

    calendrier_texte = f"{jours_abbr_str}\n{ligne_separation}\n"
    for i in range(0, len(jours_mois), 8):
        calendrier_texte += "  ".join(jours_mois[i:i+8]) + "\n"

    return calendrier_texte

@tasks.loop(time=datetime.time(POST_HOUR, POST_MINUTE))
async def send_daily_calendar():
    """ Envoie le calendrier chaque jour à l'heure définie """
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    calendrier = generer_calendrier(mois, jour_mois)
    message_immersion = random.choice(messages_accueil)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n"
                    f"📆 *Correspondance dans notre monde : {date_reelle.strftime('%d/%m/%Y')}*\n\n"
                    f"{message_immersion}",
        color=0xFFD700
    )

    embed.add_field(name="🎉 Festivité du jour", value=f"{festivite}", inline=False)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astraelis : {phase_astraelis} | Vörna : {phase_vorna}", inline=False)
    embed.add_field(name="📆 Mois en cours", value=f"```\n{calendrier}```", inline=False)
    embed.add_field(name="📅 Voir le calendrier complet", value="[🔗 Cliquez ici](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
    else:
        print("❌ Erreur : Channel introuvable ! Vérifie l'ID du canal.")

bot.run(TOKEN)

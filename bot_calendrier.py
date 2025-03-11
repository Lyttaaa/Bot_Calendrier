import os
import discord
from discord.ext import tasks, commands
import datetime
import random

TOKEN = os.getenv("TOKEN")  # Récupération du token depuis les variables d'environnement
CHANNEL_ID = 1348851808549867602  # Remplace avec l'ID de ton canal Discord

POST_HOUR = 14  # Heure en 24h (ex: 8 = 08h00 du matin)
POST_MINUTE = 33  # Minute exacte de l'envoi

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Jours et mois du calendrier de Lumharel
jours_complet = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvael", "Luméon", "Kaelios", "Eldrith"]
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois_noms = ["Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar", "Velkaris", "Nytheris", "Varneth", "Elthiris", "Zorvahl", "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"]

# Phases des lunes
phases_astraelis = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
phases_vorna = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]

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
    (1, "Aëldrin"): "Grande Récitation"
}

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
    festivite_du_jour = festivites.get((jour_mois, mois_nom), "Aucune")

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

def generate_calendar(mois_nom, jour_mois):
    """ Génère la mise en forme du calendrier avec plus d’espace entre les colonnes """
    calendrier = "\n\n"

    # En-tête avec les jours de la semaine alignés avec plus d'espace
    calendrier += "   ".join([f"{abbr:^4}" for abbr in jours_abbr]) + "\n"
    calendrier += "-" * 48 + "\n"

    # Générer les jours du mois
    ligne = ""
    for i in range(1, 33):
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
    print(f"📌 Commandes enregistrées : {[command.name for command in bot.commands]}")
    
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"📨 Channel trouvé : {channel.name} (ID: {CHANNEL_ID})")
    else:
        print("❌ Erreur : Impossible de trouver le channel. Vérifie l'ID dans ton script !")

    # Vérification et démarrage de la tâche planifiée
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
        print(f"⏰ Envoi automatique du calendrier activé pour {POST_HOUR:02d}:{POST_MINUTE:02d} chaque jour.")
    else:
        print("⚠️ La tâche d'envoi est déjà en cours.")
        
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")
    print(f"📌 Commandes enregistrées : {[command.name for command in bot.commands]}")
    
    # Vérification et démarrage de la tâche planifiée
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
        print("⏰ Envoi automatique du calendrier activé !")

@bot.command(name="calendrier")
async def calendrier(ctx):
    """ Affiche la date et le calendrier en temps réel """
    await send_calendar_message(ctx.channel)

@tasks.loop(time=datetime.time(POST_HOUR, POST_MINUTE))
async def send_daily_calendar():
    """ Vérifie et envoie automatiquement le calendrier chaque jour """
    print(f"⏳ Vérification de l'heure... Il est {datetime.datetime.now().strftime('%H:%M')}, l'envoi est prévu à {POST_HOUR:02d}:{POST_MINUTE:02d}")

    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        print(f"📨 Envoi du message automatique dans {channel.name} (ID: {CHANNEL_ID})...")
        await send_calendar_message(channel)
    else:
        print(f"❌ Erreur : Channel introuvable avec l'ID {CHANNEL_ID}. Vérifie l'ID du canal dans le script !")
        
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

    embed.add_field(name="📅 Voir le calendrier complet", value="[🔗 Cliquez ici](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    await channel.send(embed=embed)

bot.run(TOKEN)

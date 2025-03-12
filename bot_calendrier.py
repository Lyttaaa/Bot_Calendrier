import os
import discord
from discord.ext import tasks, commands
import datetime
import random
import pytz

# Vérification de l'heure système
print(f"🕒 [DEBUG] Heure système Railway : {datetime.datetime.now()}")

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1348851808549867602  

POST_HOUR = 11 
POST_MINUTE = 00

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
ref_date_irl = datetime.date(2025, 3, 12)  
ref_date_lumharel = (7, "Vækirn", 1532)  

# Messages immersifs
messages_accueil = [
    "✨ Que les vents de Lumharel vous soient favorables !",
    "🌙 Que la lumière des lunes vous guide en cette journée !",
    "🔥 Puisse la flamme de Vaek illuminer votre chemin !",
    "🌿 Que les murmures des anciens Façonneurs vous inspirent aujourd’hui !"
]

# Festivités fixes
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

### 🔹 **Convertir la date IRL en date Lumharel**
def get_lumharel_date():
    """ Calcule la date en Lumharel à partir de la date IRL du 12 mars 2025 comme référence. """
    date_actuelle = datetime.date.today()
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
    jour_semaine = jours_complet[(jour_mois - 1) % 8]  

    # 🔹 Calcul des phases lunaires basées sur le 12 mars 2025 comme référence
    jours_depuis_ref = (date_actuelle - ref_date_irl).days

    # Astrealis (cycle de 32 jours, 8 phases)
    phase_astraelis_index = (jours_depuis_ref % 32)  # Position dans le cycle de 32 jours
    phase_astraelis = phases_lune[(phase_astraelis_index * 8) // 32]  # Converti en phase

    # Vörna (cycle de 48 jours, 8 phases)
    phase_vorna_index = (jours_depuis_ref % 48)  # Position dans le cycle de 48 jours
    phase_vorna = phases_lune[(phase_vorna_index * 8) // 48]  # Converti en phase

    festivite_du_jour = festivites.get((jour_mois, mois_nom), "Aucune")

    return mois_nom, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite_du_jour, date_actuelle

### 🔹 **Générer le calendrier sous forme de tableau**
def generate_calendar(mois_nom, jour_mois):
    calendrier = "\n\n"
    calendrier += "   ".join([f"{abbr:^4}" for abbr in jours_abbr]) + "\n"
    calendrier += "-" * 48 + "\n"

    nb_jours = mois_durees[mois_nom]
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

### 🔹 **Envoi automatique**
@tasks.loop(seconds=60)
async def send_daily_calendar():
    now = datetime.datetime.now(pytz.timezone("Europe/Paris"))
    if now.hour == POST_HOUR and now.minute == POST_MINUTE:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await send_calendar_message(channel)

### 🔹 **Message du calendrier**
async def send_calendar_message(channel):
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    message_immersion = random.choice(messages_accueil)
    calendrier_formatte = generate_calendar(mois, jour_mois)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n"
                    f"📆 *Correspondance IRL : {date_reelle.strftime('%d/%m/%Y')}*\n\n"
                    f"{message_immersion}",
        color=0xFFD700
    )

    embed.add_field(name="🎉 Festivité", value=f"**{festivite}**", inline=True)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astrealis : {phase_astraelis} | Vörna : {phase_vorna}", inline=True)
    embed.add_field(name="🗓️ Mois en cours", value=f"```\n{calendrier_formatte}\n```", inline=False)

    await channel.send(embed=embed)

@bot.command(name="calendrier")
async def calendrier(ctx):
    """ Affiche la date et le calendrier en temps réel """
    await send_calendar_message(ctx.channel)
@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")

    # Vérification du channel
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"📌 [DEBUG] Message automatique prévu dans : {channel.name} (ID: {CHANNEL_ID})")
    else:
        print("❌ [ERROR] Impossible de trouver le channel. Vérifie l'ID.")

    # Vérification de l'heure d'envoi
    print(f"⏰ [DEBUG] L'envoi automatique est prévu à {POST_HOUR:02d}:{POST_MINUTE:02d} heure locale.")

    # Démarrer la tâche d'envoi automatique si elle n'est pas déjà active
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
        print("⏳ [DEBUG] Envoi automatique activé.")
    else:
        print("⚠️ [DEBUG] La tâche d'envoi est déjà en cours.")
bot.run(TOKEN)

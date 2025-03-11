import os
import discord
from discord.ext import tasks, commands
import datetime
import random

TOKEN = os.getenv("TOKEN")  # Récupération du token depuis les variables d'environnement
CHANNEL_ID = 123456789012345678  # Remplace avec l'ID de ton canal Discord

POST_HOUR = 8  # Heure d'envoi du message automatique
POST_MINUTE = 0

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
    """ Génère la mise en forme du calendrier """
    calendrier = "**Calendrier du mois :**\n"
    
    # En-tête avec les jours de la semaine
    calendrier += " | ".join(jours_abbr) + "\n"
    calendrier += "-" * 48 + "\n"

    # Générer les jours du mois
    ligne = ""
    for i in range(1, 33):
        if i == jour_mois:
            ligne += f"**[{i:2}]** | "  # Mettre en gras le jour actuel
        else:
            ligne += f" {i:2} | "
        
        # Retour à la ligne après chaque semaine de 8 jours
        if i % 8 == 0:
            calendrier += ligne.rstrip() + "\n"
            ligne = ""

    return calendrier

@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et actif !")
    print(f"📌 Commandes enregistrées : {[command.name for command in bot.commands]}")
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()

@bot.command(name="calendrier")
async def calendrier(ctx):
    """ Affiche la date et le calendrier en temps réel """
    await send_calendar_message(ctx.channel)

@bot.command(name="festivités_liste")
async def festivites_liste(ctx):
    """ Affiche la liste complète des festivités avec leurs dates """
    festivites_text = "\n".join([f"📅 **{jour} {mois}** - {nom}" for (jour, mois), nom in festivites.items()])

    embed = discord.Embed(
        title="🎊 Liste des Festivités de Lumharel",
        description=festivites_text,
        color=0xFFD700
    )

    await ctx.send(embed=embed)

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

    embed.add_field(name="🗓️ Calendrier du mois", value=f"```\n{calendrier_formatte}\n```", inline=False)

    embed.add_field(name="📅 Voir le calendrier complet", value="[🔗 Cliquez ici](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    if channel:
        await channel.send(embed=embed)
    else:
        print("❌ Erreur : Channel introuvable ! Vérifie l'ID du canal.")

@tasks.loop(time=datetime.time(POST_HOUR, POST_MINUTE))
async def send_daily_calendar():
    """ Envoie automatiquement le calendrier chaque jour """
    channel = bot.get_channel(CHANNEL_ID)
    await send_calendar_message(channel)

bot.run(TOKEN)

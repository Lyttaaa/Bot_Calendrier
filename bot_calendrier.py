import os
import discord
from discord.ext import tasks, commands
import datetime
import random

TOKEN = os.getenv("TOKEN")  # Récupération du token depuis les variables d'environnement
CHANNEL_ID = 1348851808549867602  # Remplace avec l'ID de ton canal Discord

POST_HOUR = 12  # Heure d'envoi du message automatique
POST_MINUTE = 56

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Jours et mois du calendrier de Lumharel
jours_complet = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvael", "Luméon", "Kaelios", "Eldrith"]
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

# Liste des festivités dynamiques
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
    print(f"📌 Commandes enregistrées : {[command.name for command in bot.commands]}")

@bot.command(name="calendrier")
async def calendrier(ctx):
    """ Affiche la date et le calendrier en temps réel """
    await send_daily_calendar()

@bot.command(name="calendrier_add_event")
async def calendrier_add_event(ctx, date: str, *, nom: str):
    """ Ajoute une festivité (ex: !calendrier_add_event 15/03/1532 FêteTest) """
    try:
        jour, mois_num, annee = map(int, date.split("/"))
        mois_nom = mois_noms[mois_num - 1]  # Conversion du numéro de mois en nom

        festivites[(jour, mois_nom)] = nom
        await ctx.send(f"✅ **{nom}** ajoutée au {jour} {mois_nom}, {annee} dans le Calendrier du Cycle des Souffles.")
    except (ValueError, IndexError):
        await ctx.send("⚠️ Format incorrect ! Utilisation : `!calendrier_add_event JJ/MM/AAAA NomDeLaFête`.")

@bot.command(name="calendrier_remove_event")
async def calendrier_remove_event(ctx, date: str, *, nom: str):
    """ Supprime une festivité (ex: !calendrier_remove_event 15/03/1532 FêteTest) """
    try:
        jour, mois_num, annee = map(int, date.split("/"))
        mois_nom = mois_noms[mois_num - 1]

        if (jour, mois_nom) in festivites and festivites[(jour, mois_nom)] == nom:
            del festivites[(jour, mois_nom)]
            await ctx.send(f"❌ **{nom}** supprimée du {jour} {mois_nom}, {annee}.")
        else:
            await ctx.send("⚠️ Aucune festivité trouvée avec ce nom et cette date.")
    except (ValueError, IndexError):
        await ctx.send("⚠️ Format incorrect ! Utilisation : `!calendrier_remove_event JJ/MM/AAAA NomDeLaFête`.")

@bot.command(name="calendrierlien")
async def calendrier_lien(ctx):
    """ Renvoie le lien vers le calendrier complet """
    await ctx.send("📅 **Voir le calendrier complet ici :** [🔗 Fantasy Calendar](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)")

@tasks.loop(time=datetime.time(POST_HOUR, POST_MINUTE))
async def send_daily_calendar():
    """ Envoie le calendrier chaque jour """
    mois, jour_mois, jour_semaine, phase_astraelis, phase_vorna, festivite, date_reelle = get_lumharel_date()
    message_immersion = random.choice(messages_accueil)

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, 1532 - Ère du Cycle Unifié**\n\n"
                    f"📆 *Correspondance dans notre monde : {date_reelle.strftime('%d/%m/%Y')}*\n\n"
                    f"{message_immersion}",
        color=0xFFD700
    )

    embed.add_field(name="🎉 Festivité du jour", value=f"**{festivite}**", inline=True)
    embed.add_field(name="🌙 Phases lunaires", value=f"Astraelis : {phase_astraelis}\nVörna : {phase_vorna}", inline=True)

    embed.add_field(name="📅 Voir le calendrier complet", value="[🔗 Cliquez ici](https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78)", inline=False)

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
    else:
        print("❌ Erreur : Channel introuvable ! Vérifie l'ID du canal.")

bot.run(TOKEN)

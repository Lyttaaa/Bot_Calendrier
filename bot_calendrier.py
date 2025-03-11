import discord
from discord.ext import commands, tasks
import os
import datetime
import os

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("❌ Erreur : La variable d'environnement 'TOKEN' est absente ou invalide.")
else:
    print("✅ Token chargé avec succès.")
import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")  # Récupération du token depuis Railway

intents = discord.Intents.default()
intents.message_content = True  # Active la lecture des messages pour les commandes

intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire les messages
intents.presences = True  # Facultatif, mais peut être utile
intents.members = True  # Facultatif pour gérer les membres

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} est connecté !')

    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
        print("🔄 Tâche automatique démarrée avec succès !")  # Debug
        
    await send_daily_calendar()  # 💡 Test immédiat !
    
    else:
        print("⚠️ La tâche automatique était déjà en cours !")

    # Test immédiat
    await send_daily_calendar()
async def on_ready():
    print(f'✅ {bot.user} est connecté !')
    send_daily_calendar.start()  # Démarrer la tâche automatique
    
@tasks.loop(hours=24)
async def send_daily_calendar():
    """Envoie automatiquement le message du calendrier chaque jour"""
    print("⏳ Tentative d'envoi du calendrier...")
    
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"📢 Message envoyé dans : {channel.name}")  # Debug
        await channel.send(embed=generate_calendar_embed())
    else:
        print("❌ Erreur : Le bot ne trouve pas le salon ! Vérifie l'ID du salon.")
CHANNEL_ID = 1348851808549867602  # Remplace avec l'ID du salon où poster le message

# Jours et mois de Lumharel
jours = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois = [
    "Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar",
    "Velkaris", "Nytheris", "Varneth", "Elthiris", "Zorvahl",
    "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"
]

@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user}')

@bot.command()
async def calendrier(ctx):
    """Affiche le calendrier en embed sans image"""

    # Définition de la date actuelle fictive
    jour = 15
    mois_actuel = "Vækirn"
    annee = 1532
    ere = "Cycle Unifié"
    festivite = "Aucune"
    phases_lunaires = "Astraelis : 🌔 | Vörna : 🌘"

    # Formatage du calendrier en tableau texte
    calendrier_texte = "**" + mois_actuel + " - " + str(annee) + "**\n"
    calendrier_texte += "```\n"
    calendrier_texte += " ".join(jours) + "\n"

    ligne = ""
    for i in range(1, 33):  # 32 jours
        if i == jour:
            ligne += f"[{i:2d}] "  # Met le jour actuel en surbrillance
        else:
            ligne += f"{i:2d}  "
        
        if i % 8 == 0:  # Nouvelle ligne tous les 8 jours
            calendrier_texte += ligne.strip() + "\n"
            ligne = ""

    calendrier_texte += "```"

    # Création de l'embed
    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"**Nous sommes le {jours[jour % 8]} {jour} {mois_actuel}, {annee} - Ère du {ere}**\n\n✨ *Que les vents de Lumharel vous soient favorables !*",
        color=0xFFD700
    )
    embed.add_field(name="🎊 Festivité", value=festivite, inline=True)
    embed.add_field(name="🌙 Phases Lunaires", value=phases_lunaires, inline=True)
    embed.add_field(name="📆 Mois en cours", value=calendrier_texte, inline=False)
    embed.set_footer(text="📜 Suivez le cycle, suivez le souffle...")

    await ctx.send(embed=embed)

@bot.command()
async def calendrierlien(ctx):
    """Renvoie le lien vers le calendrier complet."""
    await ctx.send("🔗 **Consultez le calendrier complet ici :** https://app.fantasy-calendar.com/calendars/1ead959c9c963eec11424019134c7d78")
@tasks.loop(hours=24)
async def send_daily_calendar():
    """Envoie automatiquement le message du calendrier chaque jour"""
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=generate_calendar_embed())

def generate_calendar_embed():
    """Génère l'embed du calendrier"""
    today = datetime.datetime.utcnow().day
    mois_actuel = "Vækirn"
    annee = 1532
    ere = "Cycle Unifié"
    festivite = "Aucune"
    phases_lunaires = "Astraelis : 🌔 | Vörna : 🌘"

    embed = discord.Embed(
        title="📜 Calendrier du Cycle des Souffles",
        description=f"**Nous sommes le {today} {mois_actuel}, {annee} - Ère du {ere}**\n\n✨ *Que les vents de Lumharel vous soient favorables !*",
        color=0xFFD700
    )
    embed.add_field(name="🎊 Festivité", value=festivite, inline=True)
    embed.add_field(name="🌙 Phases Lunaires", value=phases_lunaires, inline=True)
    embed.set_footer(text="📜 Suivez le cycle, suivez le souffle...")

    return embed
# Démarrer le bot
bot.run(TOKEN)

import discord
from discord.ext import commands, tasks
import os
import datetime

# Charger le token du bot depuis les variables d'environnement
TOKEN = os.getenv("TOKEN")

# Activer les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True

# Création du bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ID du salon Discord où envoyer le message automatique
CHANNEL_ID = 123456789012345678  # Remplace avec ton vrai ID de salon !

# ✅ 1. Définition de la tâche automatique avant on_ready()
@tasks.loop(hours=24)
async def send_daily_calendar():
    """Envoie automatiquement le message du calendrier chaque jour"""
    print("⏳ Tentative d'envoi du calendrier...")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"📢 Message envoyé dans : {channel.name}")  # Debug dans Railway Logs
        await channel.send(embed=generate_calendar_embed())
    else:
        print("❌ Erreur : Le bot ne trouve pas le salon ! Vérifie l'ID du salon.")

# ✅ 2. Fonction qui génère l'embed du calendrier
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

# ✅ 3. on_ready() pour démarrer la tâche et tester immédiatement
@bot.event
async def on_ready():
    print(f'✅ {bot.user} est connecté !')

    # Vérifie si la tâche automatique tourne déjà
    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
        print("🔄 Tâche automatique démarrée avec succès !")
    else:
        print("⚠️ La tâche automatique était déjà en cours !")

    # 💡 Test immédiat : le bot enverra un message dès son démarrage
    await send_daily_calendar()

# ✅ 4. Commande manuelle pour afficher le calendrier sur demande
@bot.command()
async def calendrier(ctx):
    """Commande !calendrier pour afficher le calendrier"""
    await ctx.send(embed=generate_calendar_embed())

# ✅ 5. Lancer le bot
bot.run(TOKEN)

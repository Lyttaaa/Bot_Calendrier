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

bot = commands.Bot(command_prefix="!", intents=intents)

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

# Démarrer le bot
bot.run(TOKEN)

import os
import discord
from discord.ext import tasks, commands
import datetime
import random

# Configuration du bot
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ Erreur : Aucun token trouvé ! Vérifie tes variables d'environnement.")
else:
    print(f"🔑 Token chargé : {TOKEN[:5]}... (caché pour sécurité)")
  
CHANNEL_ID = 1348851808549867602  # Remplace avec l'ID de ton salon

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Jours et Mois
jours_complets = ["Tellion", "Sildrien", "Vaeldris", "Nythariel", "Zorvael", "Luméon", "Kaelios", "Eldrith"]
jours_abbr = ["Tel", "Sil", "Vae", "Nyt", "Zor", "Lum", "Kae", "Eld"]
mois_lumharel = ["Orréa", "Thiloris", "Vækirn", "Dornis", "Solvannar", "Velkaris", "Nytheris", "Varneth", 
                 "Elthiris", "Zorvahl", "Draknar", "Umbraël", "Aëldrin", "Kaelthor", "Eldros"]

# Variantes de messages immersifs
messages_immersifs = [
    "✨ Que les vents de Lumharel vous soient favorables !",
    "🌿 Puisse la nature guider vos pas en cette journée.",
    "🔥 Que la flamme de la connaissance éclaire votre chemin.",
    "🌙 Sous la lumière des lunes, avancez avec sagesse.",
    "🔮 Le destin tisse ses fils, soyez prêt à en saisir l'opportunité.",
    "🌀 Que le cycle des souffles vous inspire aujourd’hui !"
]

@tasks.loop(hours=24)
async def send_daily_calendar():
    """Envoie automatiquement le calendrier chaque jour dans un embed"""
    print("⏳ Tentative d'envoi du calendrier...")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"📢 Message envoyé dans : {channel.name}")

        # Obtenir la date actuelle
        now = datetime.datetime.utcnow()
        jour_mois = now.day
        jour_semaine = jours_complets[now.weekday() % 8]  # Assure une rotation correcte
        mois = mois_lumharel[(now.month - 1) % 15]  # Adapte aux 15 mois du cycle
        annee = 1532  # (Peut être dynamique si besoin)
        ere = "Cycle Unifié"

        # Déterminer une phrase immersive aléatoire
        message_immersif = random.choice(messages_immersifs)

        # Simuler la phase lunaire (remplacer par de vrais calculs si besoin)
        phases_lunaires = "Astraelis : 🌔 | Vörna : 🌘"

        # Définir une festivité (Exemple statique, peut être dynamique)
        festivite = "Aucune"  # Mettre le vrai nom si une festivité a lieu aujourd’hui

        # Générer les jours du mois avec highlight du jour actuel
        jours_mois = []
        for i in range(1, 33):  # Boucle de 1 à 32 jours du mois
            jour_str = f"{i:2}"  # Garde l'alignement
            if i == jour_mois:
                jour_str = f"[{jour_str}]"  # Met en gras le jour actuel
            jours_mois.append(jour_str)

        # Construction du calendrier sous forme de colonnes
        calendrier_texte = " | ".join(jours_abbr) + "\n"
        calendrier_texte += "-" * len(calendrier_texte) + "\n"

        for i in range(0, len(jours_mois), 8):  # Groupe les jours par semaines de 8 jours
            semaine = " | ".join(jours_mois[i:i+8])
            calendrier_texte += semaine + "\n"

        # Création de l'embed avec l'ordre exact demandé
        embed = discord.Embed(
            title="📜 Calendrier du Cycle des Souffles",
            description=f"📅 **Nous sommes le {jour_mois} ({jour_semaine}) de {mois}, {annee} - Ère du {ere}**\n\n{message_immersif}",
            color=0xFFD700
        )
        embed.add_field(name="🎊 Festivités", value=festivite, inline=True)
        embed.add_field(name="🌙 Phases Lunaires", value=phases_lunaires, inline=True)
        embed.add_field(name="📆 Mois en cours", value=f"```\n{calendrier_texte}```", inline=False)
        embed.set_footer(text="📜 Suivez le cycle, suivez le souffle...")

        await channel.send(embed=embed)
    else:
        print("❌ Erreur : Le bot ne trouve pas le salon ! Vérifie l'ID du salon.")

@bot.event
async def on_ready():
    print(f'✅ {bot.user} est connecté !')

    if not send_daily_calendar.is_running():
        send_daily_calendar.start()
        print("🔄 Tâche automatique démarrée avec succès !")
    else:
        print("⚠️ La tâche automatique était déjà en cours !")

    await send_daily_calendar()  # 💡 Test immédiat au démarrage !

bot.run(TOKEN)

import asyncio
import discord
from discord.ext import commands

# ── Config ─────────────────────────────────────────────────────────────────────
TOKEN        = "MTQ4Mjg1MTcxNTM2NjUxOTA1NQ.GE3PaC.tztESpCXhtg4bc7pAynSZwTma0j9jraqrcavVg"
OWNER_ID     = 1456322226491101224
SPAM_OPTIONS = [1, 5, 10, 20, 50, 100]

# ── Client setup ───────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?unused", intents=intents)

# ── Spam panel ─────────────────────────────────────────────────────────────────
class SpamButtons(discord.ui.View):
    def __init__(self, message: str):
        super().__init__(timeout=120)
        self.message = message
        for count in SPAM_OPTIONS:
            style = (
                discord.ButtonStyle.secondary if count == 1 else
                discord.ButtonStyle.primary   if count <= 10 else
                discord.ButtonStyle.danger
            )
            button = discord.ui.Button(label=f"Spam {count}", style=style)
            button.callback = self._make_callback(count)
            self.add_item(button)

    def _make_callback(self, n: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != OWNER_ID:
                return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
            await interaction.response.defer(ephemeral=True)
            # Fire all messages concurrently — maximum speed
            await asyncio.gather(*[interaction.followup.send(self.message) for _ in range(n)])
            await interaction.followup.send(f"✅ Done — sent {n}.", ephemeral=True)
        return callback

# ── Slash commands ─────────────────────────────────────────────────────────────
@bot.tree.command(name="spam", description="Open the spam panel")
@discord.app_commands.describe(message="Message to spam")
@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_spam(interaction: discord.Interaction, message: str):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(
        f"📨 **Spam Panel** — `{message}`",
        view=SpamButtons(message),
        ephemeral=True
    )

@bot.tree.command(name="spamnow", description="Spam immediately")
@discord.app_commands.describe(
    count="Number of messages (max 500)",
    message="Message to spam"
)
@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_spamnow(interaction: discord.Interaction, count: int, message: str):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ Not authorized.", ephemeral=True)
    if not 1 <= count <= 500:
        return await interaction.response.send_message("❌ Count must be 1–500.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    # Fire all messages concurrently — maximum speed
    await asyncio.gather(*[interaction.followup.send(message) for _ in range(count)])
    await interaction.followup.send(f"✅ Done — sent {count}.", ephemeral=True)

# ── Events ─────────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"✅  {bot.user} ({bot.user.id})")
        print(f"    Install URL: https://discord.com/oauth2/authorize?client_id={bot.user.id}&integration_type=1&scope=applications.commands")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

bot.run(TOKEN)

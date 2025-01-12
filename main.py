import discord
import os
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
from myserver import server_on

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # เริ่มต้น Task Loop เมื่อบอทพร้อม
    send_daily_checklist.start()

@tasks.loop(time=time(16, 0))  # กำหนดเวลา 20:13
async def send_daily_checklist():
    # ระบุช่องที่ต้องการส่งข้อความ
    channel = bot.get_channel(1327977708713541672)  # ใส่ Channel ID ที่ต้องการส่งข้อความ
    if channel:
        # สร้าง Embed สำหรับ Checklist
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        embed = discord.Embed(
            title="Checklist ที่ต้องทำ",
            description="",
            color=0x2ecc71
        )
        embed.add_field(name="dary quest", value="\u200b", inline=False)
        embed.add_field(name="Time", value=current_time, inline=False)
        embed.add_field(
            name="Teams",
            value="🔵 องค์ที่เป็นนิรันดร์\n🟡 ส่งกล่องราชวงศ์\n🔴 รายวันกิจกรรม",
            inline=False
        )
        message = await channel.send(embed=embed)

        # เพิ่มปุ่ม Reaction
        reactions = ["🔵", "🟡", "🔴"]
        for reaction in reactions:
            await message.add_reaction(reaction)

        # เก็บข้อมูลใน Message Cache
        bot.message_cache = message

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    message = reaction.message
    if hasattr(bot, "message_cache") and message.id == bot.message_cache.id:
        embed = message.embeds[0]
        color_name = ""

        # ตรวจสอบ Reaction และเพิ่มชื่อผู้ใช้
        if reaction.emoji == "🔵":
            color_name = "🔵 องค์ที่เป็นนิรันดร์"
        elif reaction.emoji == "🟡":
            color_name = "🟡 ส่งกล่องราชวงศ์"
        elif reaction.emoji == "🔴":
            color_name = "🔴 รายวันกิจกรรม"

        if color_name:
            for field in embed.fields:
                if color_name in field.name:
                    field.value += f"\n- {user.name}"
                    break

            await message.edit(embed=embed)

# ใส่ Token ของบอทของคุณที่นี่
bot.run(os.getenv('TOKEN'))


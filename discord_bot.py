import disnake
from disnake import Embed
from disnake.ext import commands

intents = disnake.Intents.all()
# activity = disnake.Game(name="app")
status = disnake.Status.do_not_disturb
bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    # activity=activity,
    status=status,
    test_guilds=[] # ID channel
)

# LOG_CHANNEL_ID = 

@bot.event
async def on_ready():
    print(f"Бот {bot.user.name}, успешно запущен!")



### КОД ДЛЯ ЛОГИРОВАНИЯ ДЕЙСТВИЙ ПОЛЬЗОВАТЕЛЯ

# @bot.event
# async def on_message_delete(message: disnake.Message):
#     if message.author.bot:
#         return
#     log_message = f'Пользователь `{message.author}` удалил сообщение `{message.content}` в  {message.jump_url}  канале!'
#     log_channel = bot.get_channel(LOG_CHANNEL_ID)
#     if log_channel:
#         await log_channel.send(log_message)
#     else:
#         print(f'Ошибка: Не удалось найти канал с ID {LOG_CHANNEL_ID} для логирования!')

# @bot.event
# async def on_slash_command(ctx: disnake.ApplicationCommandInteraction):
#     log_channel = bot.get_channel(LOG_CHANNEL_ID)
#     if log_channel:
#         command_name = ctx.data.name
#         options = ctx.data.options
#         channel_link = ctx.channel.mention
#         message_link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.id}"
#         message_log = None

#         if command_name == 'avatar':
#             if options:
#                 param_name = options[0]['name']
#                 param_value = options[0]['value']

#                 if param_name == 'member':
#                     member = await bot.fetch_user(param_value)
#                     message_log = f"Пользователь `{ctx.author.name}` использовал команду `{command_name}` `{param_name}` `{member.name}` в  {message_link}  канале!"

#         elif command_name == 'say' or command_name == 'info':
#             if options:
#                 param_name = options[0]['name']
#                 param_value = options[0]['value']
#                 message_log = f"Пользователь `{ctx.author.name}` использовал команду `{command_name}` `{param_name}` `{param_value}` в  {message_link}  канале!"

#         if message_log:
#             await log_channel.send(message_log)

# @bot.event
# async def on_raw_reaction_add(payload: disnake.RawReactionActionEvent):
#     guild = bot.get_guild(payload.guild_id)
#     channel = guild.get_channel(payload.channel_id)
#     message = await channel.fetch_message(payload.message_id)
#     user = guild.get_member(payload.user_id)

#     if user.bot:
#         return
#     emoji = payload.emoji
#     message_link = f"https://discord.com/channels/{guild.id}/{channel.id}/{message.id}"
#     log_message = f'Пользователь `{user}` отреагировал « {emoji} » на сообщение в  {message_link}  канале!'
#     log_channel = bot.get_channel(LOG_CHANNEL_ID)
#     if log_channel:
#         await log_channel.send(log_message)

### КОД ДЛЯ ЛОГИРОВАНИЯ ДЕЙСТВИЙ ПОЛЬЗОВАТЕЛЯ



@bot.slash_command(description="Полностью удалить все сообщения в канале")
async def clear(ctx, channel: disnake.TextChannel = commands.Param(description="Укажите канал, в котором хотите удалить сообщения")):
    await channel.purge()
    await ctx.send(f'Успешно очищено канал  {channel.mention}  от сообщений.', ephemeral=True)

@bot.slash_command(description="Скачать аватар пользователя")
async def avatar(interaction: disnake.ApplicationCommandInteraction, member: disnake.Member = commands.Param(description="Укажите пользователя для получения аватара")):
    member = member or interaction.author
    embed = Embed(
        title=f"Аватар – {member}",
        color=0x2F3136
    )
    embed.set_image(url=member.display_avatar.url)
    embed.set_footer(text="Нажмите кнопку ниже, чтобы скачать аватар")
    download_button = disnake.ui.Button(
        style=disnake.ButtonStyle.link,
        label="⬇️ Скачать аватар",
        url=member.display_avatar.url
    )
    await interaction.response.send_message(embed=embed, components=[disnake.ui.ActionRow(download_button)], ephemeral=True)

@bot.slash_command(description="Получить информацию о пользователе по ID")
async def info(interaction: disnake.ApplicationCommandInteraction, member_id: str = commands.Param(description="Укажите ID пользователя для получения информации")):
    try:
        member_id = int(member_id)
        user = await bot.fetch_user(member_id)
    except ValueError:
        await interaction.response.send_message("Введите корректный числовой ID пользователя.", ephemeral=True)
        return
    except disnake.NotFound:
        await interaction.response.send_message("Пользователь не найден.", ephemeral=True)
        return
    
    created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")

    embed = disnake.Embed(
        title=f"Информация о пользователе {user}",
        color=disnake.Color.blurple()
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="Имя", value=user.name, inline=True)
    embed.add_field(name="Никнейм", value=user.display_name, inline=True)
    embed.add_field(name="ID пользователя", value=str(user.id), inline=True)
    embed.add_field(name="Дата регистрации", value=created_at, inline=False)

    download_button = disnake.ui.Button(
        style=disnake.ButtonStyle.link,
        label="⬇️ Скачать аватар",
        url=user.display_avatar.url
    )
    await interaction.response.send_message(
        embed=embed,
        components=[disnake.ui.ActionRow(download_button)],
        ephemeral=True
    )

@bot.slash_command(description="Повторить указанный текст")
async def say(interaction: disnake.ApplicationCommandInteraction, message: str = commands.Param(description="Укажите текст который, хотите повторить")):
    await interaction.response.defer()
    await interaction.followup.send(message)

bot.run('TOKEN')
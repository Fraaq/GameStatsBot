import os
import a2s
import discord
import database_handler as db
import embeds as emb
import json
from discord.ext import commands
from dotenv import load_dotenv
from validators import validate_user_server, validate_server_argument, check_user_role, ERROR_COLOR

# Constants
SCRIPT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
MAP_THUMBNAILS_DIR = f'{SCRIPT_DIRECTORY}/map-thumbnails/'
GAMES_IN_THUMBNAILS_DIR = os.listdir(MAP_THUMBNAILS_DIR)
NOT_ALLOWED_CHAR_IN_DIR = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
ALLOWED_PHOTO_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')
BOT_PREFIX = "!"

# Load discord token (API) from env
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Load discord intents
intents = discord.Intents.default()
intents.message_content = True

# Define discord bot
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)


# Create default config for the server, when the bot is added
@bot.event
async def on_guild_join(guild):
    db.create_default_config(guild.id)


# Create default config if not exists when discord server is available
@bot.event
async def on_guild_available(guild):
    db.create_default_config(guild.id)


# Read all commands and their help messages from json and if not command in json insert it
@bot.event
async def on_ready():
    with open('help_messages.json', 'r') as json_file:
        commands_help = json.load(json_file)

    for command in bot.commands:
        if command.name not in commands_help.keys():
            commands_help[command.name] = {"help_message": "", "usage": "", "example": ""}

    with open('help_messages.json', 'w') as json_file:
        json.dump(commands_help, json_file, indent=4, sort_keys=True)


@bot.command(name='help')
async def help_func(ctx, command_name: str = None):
    """Displays a list of commands and their usage"""

    # If user specify command for help message
    if command_name:
        command = bot.get_command(command_name)

        if command:
            with open('help_messages.json', 'r') as json_file:
                help_messages = json.load(json_file)

            command_help = help_messages[command_name]["help_message"]
            command_usage = help_messages[command_name]["usage"]
            command_example = help_messages[command_name]["example"]

            await emb.send_command_help(ctx, BOT_PREFIX + command_name, command_help, command_usage, command_example)

        else:
            await emb.send_embed(ctx, title="Command not found", color=ERROR_COLOR,
                                 description="I'm sorry, but the command was not found. If you need "
                                             f"assistance, please type `{BOT_PREFIX}help` "
                                             "to display all available commands.")

    # If user don't specify exactly command for help message send generic help
    else:
        await emb.send_help_embed(ctx, BOT_PREFIX)


@bot.command(name='servers')
async def servers_list_func(ctx):
    """Displays all available game servers"""

    servers = db.all_game_servers(ctx.guild.id)

    if servers:
        servers_str = ', '.join([server for server in servers])
        await emb.send_embed(ctx, title=":mag_right: Servers List", description=f"`{servers_str}`")

    else:
        await emb.send_embed(ctx, title="No servers available",
                             description="Sorry, no servers are currently available.",
                             color=ERROR_COLOR)


@bot.command(name='stats')
@validate_server_argument
async def server_stats_func(ctx, server_name: str = None, server_info: dict = None):
    """Returns information about a game server."""

    ip_and_port = f"{server_info['ip']}:{server_info['port']}"
    stats = a2s.info((server_info["ip"], server_info["port"]))
    game_name = ''.join([char for char in stats.game if char not in NOT_ALLOWED_CHAR_IN_DIR])
    all_thumbnails = []
    map_thumbnail = None

    if game_name in GAMES_IN_THUMBNAILS_DIR:
        all_thumbnails = os.listdir(f'{MAP_THUMBNAILS_DIR}/{game_name}')

    # Find thumbnail for server map
    for extension in ALLOWED_PHOTO_EXTENSIONS:
        map_with_extension = stats.map_name + extension

        # Check if server game is in thumbnails dir and map name in server game dir
        if game_name in GAMES_IN_THUMBNAILS_DIR and map_with_extension in all_thumbnails:
            map_thumbnail = f'{MAP_THUMBNAILS_DIR}/{game_name}/{map_with_extension}'
            break

    await emb.send_stats_embed(ctx, game=stats.game, server_name=stats.server_name, ip=ip_and_port,
                               description=server_info["description"],
                               game_map=stats.map_name, players=f"{stats.player_count}/{stats.max_players}",
                               map_thumbnail=map_thumbnail)


@bot.command(name='players')
@validate_server_argument
async def players_info_func(ctx, server_name: str = None, server_info: dict = None):
    """Returns a list of players on the game server, along with their scores and playtime"""

    players = a2s.players((server_info["ip"], server_info["port"]))
    players = [player for player in players if player.name]

    if players:
        players_sorted = sorted(players, key=lambda player: player.score, reverse=True)

        player_names = "\n".join([player.name for player in players_sorted])
        player_scores = "\n".join([str(player.score) for player in players_sorted])
        player_playtime = "\n".join([f"{int(player.duration // 60)} min" for player in players_sorted])

        await emb.send_players_list_embed(ctx, player_names=player_names, player_scores=player_scores,
                                          player_playtime=player_playtime)

    else:
        await emb.send_embed(ctx, title="No active players on the server", color=ERROR_COLOR)


@bot.command(name="add_server")
@check_user_role
@validate_user_server
async def add_server_func(ctx, server_name: str, server_ip: str, server_description: str):
    """Add a game server to the list"""

    ip, port = server_ip.split(":")
    description_str = ' '.join(server_description)
    server_add = db.add_game_server(ctx.guild.id, server_name, ip, int(port), description_str)

    if server_add:
        await emb.send_embed(ctx, title=f"You have successfully added server {server_name}",
                             color=discord.Color.green())

    else:
        await emb.send_embed(ctx, title="Sorry, something went wrong", color=ERROR_COLOR)


@bot.command(name="del_server")
@check_user_role
async def del_server_func(ctx, server_name: str = None):
    """Deletes a game server from the list"""

    server_exists = db.find_game_server(ctx.guild.id, server_name)

    if server_exists:
        server_deleted = db.del_game_server(ctx.guild.id, server_name)

        if server_deleted:
            await emb.send_embed(ctx, title=f"You have successfully deleted server {server_name}",
                                 color=discord.Color.green())
        else:
            await emb.send_embed(ctx, title="Sorry, something went wrong")

    else:
        all_servers = ', '.join([server for server in db.all_game_servers(ctx.guild.id)])
        await emb.send_embed(ctx, title="You need to choose one of this servers",
                             description=f"`{all_servers}`", color=ERROR_COLOR)


@bot.command(name="info")
@validate_server_argument
async def info_server_func(ctx, server_name: str = None, server_info: dict = None):
    """Display saved information about a game server"""

    await emb.send_info_embed(ctx, server_name, server_info)


bot.run(DISCORD_TOKEN)

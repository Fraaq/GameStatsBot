import ipaddress
import discord
import re
from embeds import send_embed
import database_handler as db

ERROR_COLOR = discord.Color.red()
DISCORD_MANAGE_ROLE = "games server manager"


def validate_domain(domain_name: str) -> bool:
    """Validate if string can be domain name"""
    regex = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
    p = re.compile(regex)

    if re.search(p, domain_name):
        return True

    else:
        return False


def validate_ip(ip: str) -> bool:
    """Validate if string is valid ip address"""
    try:
        ipaddress.ip_address(ip)
        return True

    except ValueError:
        return False


def validate_port(port) -> bool:
    """Validate if port is valid"""
    if 0 < int(port) < 65535:
        return True

    else:
        return False


def validate_user_server(func):
    """Decorator that checks if the user's server has valid parameters."""
    async def wrapper(ctx, server_name: str = None, server_ip: str = None, *server_description):
        if all([server_name, server_ip, server_description]):
            try:
                ip, port = server_ip.split(":")

            except ValueError:
                await send_embed(ctx, color=ERROR_COLOR, title="Bad Server IP",
                                 description="You need to write server ip with port "
                                             "something like this : **10.20.30.40:27015**")
                return

            is_valid_ip = validate_ip(ip)
            is_valid_port = validate_port(port)
            is_valid_domain = validate_domain(server_ip)
            is_valid_description = len(server_description) < 35
            server_exists = db.find_game_server(ctx.guild.id, server_name)

            if (is_valid_ip or is_valid_domain) and (is_valid_port and not server_exists and is_valid_description):
                await func(ctx, server_name, server_ip, server_description)

            elif not is_valid_ip and not is_valid_domain:
                await send_embed(ctx, title="Your ip address is not valid", color=ERROR_COLOR)

            elif not is_valid_port:
                await send_embed(ctx, title="Your port is not valid", color=ERROR_COLOR)

            elif server_exists:
                await send_embed(ctx, title="Server name already in servers", color=ERROR_COLOR)

            elif len(server_description) > 35:
                await send_embed(ctx, title="The description must be shorter than 35 words.", color=ERROR_COLOR)

        else:
            await send_embed(ctx, title="You didn't write required arguments", color=ERROR_COLOR,
                             description="Use this command like this: `!add_server server-name "
                                         "10.20.30.40:27015 Your description of the server`")

    return wrapper


def validate_server_argument(func):
    """Decorator that checks server argument that user wrote and add server info from database to function"""

    async def wrapper(ctx, server_name: str = None):
        try:
            guild_id = ctx.guild.id
            game_servers = db.all_game_servers(guild_id)

            if not server_name and len(game_servers) > 1:
                all_servers = ', '.join([server for server in game_servers])
                await send_embed(ctx, title="You need to choose one of this servers",
                                 description=f"`{all_servers}`", color=ERROR_COLOR)

            elif not server_name and len(game_servers) == 1:
                server_name = game_servers[0]

                server = db.find_game_server(guild_id, server_name)

                await func(ctx, server_name, server)

            elif server_name in game_servers and len(game_servers) >= 1:
                server = db.find_game_server(guild_id, server_name)

                await func(ctx, server_name, server)

            elif server_name not in game_servers:
                await send_embed(ctx, title="Server not found", color=ERROR_COLOR)

            else:
                await send_embed(ctx, title="Sorry, something went wrong", color=ERROR_COLOR)

        except TimeoutError:
            await send_embed(ctx, title="Server is offline", color=ERROR_COLOR)

    return wrapper


def check_user_role(func):
    """Check if user has required role to manage games server"""

    async def wrapper(ctx, *args):
        all_user_roles = [role.name.lower() for role in ctx.author.roles]

        if DISCORD_MANAGE_ROLE.casefold() in all_user_roles:
            await func(ctx, *args)

        else:
            await send_embed(ctx, color=ERROR_COLOR,
                             title="You don't have required role",
                             description=f"You don't have **{DISCORD_MANAGE_ROLE}** role")

    return wrapper

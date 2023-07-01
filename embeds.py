import discord
from datetime import datetime
from typing import Union


def send_help_embed(ctx, bot_prefix: str):
    embed = discord.Embed(title="Help message",
                          description="Hello! I'm a Discord bot designed to assist "
                                      "you in managing game servers. I can perform multiple "
                                      "tasks to enhance your gaming experience. For a more detailed explanation"
                                      f"of a specific command, use `{bot_prefix}help <command>`.",
                          color=discord.Color.blurple())

    embed.add_field(name=":gear: Manage Games Server", inline=False,
                    value=f"`{bot_prefix}servers`, `{bot_prefix}add_server`, `{bot_prefix}del_server`")
    embed.add_field(name=":page_facing_up: Get information", value=f"`{bot_prefix}stats`, `{bot_prefix}info`, "
                                                                   f"`{bot_prefix}players`", inline=False)

    return ctx.send(embed=embed)


def send_command_help(ctx, command_with_prefix: str, command_help: str, command_usage: str, command_example: str):
    embed = discord.Embed(title=command_with_prefix, description=command_help, color=discord.Color.blurple())
    embed.add_field(name="Usage", value=f"`{command_with_prefix} {command_usage}`", inline=True)
    embed.add_field(name="Example", value=f"`{command_with_prefix} {command_example}`")
    
    return ctx.send(embed=embed)


def send_embed(ctx, title: str, description: str = None, color: Union[int, discord.Colour, None] = 0x0391fb):
    embed = discord.Embed(title=title, description=description, color=color)

    return ctx.send(embed=embed)


def send_stats_embed(ctx, ip: str, description: str, game: str, server_name: str, game_map: str, players: str,
                     map_thumbnail: str, color: Union[int, discord.Colour, None] = 0x0391fb):

    embed = discord.Embed(title=":bar_chart: Server Stats", description=description, color=color)
    embed.add_field(name=":video_game: Game", value=game, inline=False)
    embed.add_field(name=":label: Server Name", value=server_name, inline=False)
    embed.add_field(name=":mirror_ball: Server ip", value=ip, inline=False)
    embed.add_field(name=":map: Map", value=game_map, inline=False)
    embed.add_field(name=":trophy: Players", value=players, inline=False)
    embed.timestamp = datetime.utcnow()

    if map_thumbnail:
        thumbnail_file = discord.File(map_thumbnail)
        embed.set_image(url=f"attachment://{thumbnail_file.filename}")

        return ctx.send(embed=embed, file=thumbnail_file)

    else:
        return ctx.send(embed=embed)


def send_players_list_embed(ctx, player_names, player_scores, player_playtime):
    embed = discord.Embed(title=":joystick: Player List",
                          description="This is a list of players with their scores and uptimes",
                          color=discord.Color.blue())

    embed.add_field(name="Username", value=player_names, inline=True)
    embed.add_field(name="Score", value=player_scores, inline=True)
    embed.add_field(name="Play Time", value=player_playtime, inline=True)

    return ctx.send(embed=embed)


def send_info_embed(ctx, server_name: str, server_info: dict):
    embed = discord.Embed(title=":hammer_pick: Server Information",
                          description="This is stored information about server",
                          color=discord.Color.blue())

    embed.add_field(name=":label: Server name", value=server_name, inline=False)
    embed.add_field(name=":pencil: Server description", value=server_info['description'], inline=False)
    embed.add_field(name=":mirror_ball: Server ip", value=f"{server_info['ip']}:{server_info['port']}", inline=False)

    return ctx.send(embed=embed)

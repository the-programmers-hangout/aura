import yaml
from discord.ext import commands

from cogs.karma.checker import KarmaChecker
from cogs.karma.leaderboard import Leaderboard
from cogs.karma.provider import Helpful, Informative, Kind, Creative, Funny

if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    client = commands.Bot(command_prefix=data_loaded['prefix'])
    client.add_cog(Helpful(client))
    client.add_cog(Informative(client))
    client.add_cog(Kind(client))
    client.add_cog(Creative(client))
    client.add_cog(Funny(client))
    client.add_cog(KarmaChecker(client))
    client.add_cog(Leaderboard(client))
    client.run(data_loaded['token'])

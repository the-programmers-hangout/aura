import pymongo

from core.database import Database
from core.model.member import KarmaMember
from util.config import ConfigManager


class KarmaService:

    def __init__(self):
        self._config = ConfigManager().config
        self._karma = Database(self._config['database']['host'], self._config['database']['port'],
                               self._config['database']['username'], self._config['database']['password'],
                               self._config['database']['name']).db.karma
        self._filter_query = dict(guild_id="", member_id="", karma_type="")
        self._increase_karma = {"$inc": {'karma': int(1)}}

    def upsert_karma_member(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['karma_type'] = member.karma_type
        self._karma.update_one(filter=self._filter_query, update=self._increase_karma,
                               upsert=True)

    def get_top_karma_members(self, guild_id: str, limit: int, karma_type: str):
        filter_guild = dict(guild_id=guild_id, karma_type=karma_type)
        print(filter_guild)
        return self._karma.find(filter_guild).sort([('karma', pymongo.ASCENDING)]).limit(limit)

    def delete_karma_member(self, member: KarmaMember):
        print()

    def set_karma(self, member: KarmaMember, new_karma: int):
        print()

    def get_karma_from_karma_member(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['karma_type'] = member.karma_type
        document = self._karma.find_one(filter=self._filter_query)
        if document is None:
            return 0
        else:
            return document['karma']

    def cooldown_karma_giving_ability(self, member: KarmaMember):
        print()

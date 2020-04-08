from core.database import Database
from core.model.karma_member import KarmaMember


class KarmaService:

    def __init__(self):
        self._db = Database('localhost', 27017, 'aura.db').db
        self._filter_query = {"guild_id": "{}",
                              "member_id": "{}",
                              "karma_type": "{}"}
        self._increase_karma = {"$inc: { karma: 1 }"}

    def upsert_karma_member(self, member: KarmaMember):
        karma = self._db.karma
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['karma_type'] = member.karma_type
        karma.update_one(filter=self._filter_query, update=self._increase_karma,
                         upsert=True)

    def delete_karma_member(self, member: KarmaMember):
        print()

    def reset_karma_member(self, member: KarmaMember):
        print()

    def get_karma_from_karma_member(self, member: KarmaMember):
        self._filter_query['guild_id'] = member.guild_id
        self._filter_query['member_id'] = member.member_id
        self._filter_query['karma_type'] = member.karma_type
        karma = self._db.karma.find_one(filter=self._filter_query)
        return karma['karma']

    def cooldown_karma_giving_ability(self, member: KarmaMember):
        print()

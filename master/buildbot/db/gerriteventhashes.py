
import json

import sqlalchemy as sa
import sqlalchemy.exc

from buildbot.db import base


class EventDict(dict):
    pass


class GerritEventHashConnectorComponent(base.DBConnectorComponent):

    def thdInsertEventHash(self, conn, event_hash):
        """
        Insert an event hash into the database. Return true if insert was
        successful

        INSERT INTO gerrit_event_hashes SET event_hash=?
        """

        table = self.db.model.gerriteventhashes
        try:
            conn.execute(table.insert(), event_hash=event_hash)
            return True
        except (sqlalchemy.exc.IntegrityError):
            pass

        return False

    def insertEventHash(self, event_hash):
        def thd(conn):
            return self.thdInsertEventHash(conn, event_hash)
        return self.db.pool.do(thd)

    def _test_timing_hook(self, conn):
        # called so tests can simulate another process inserting a database row
        # at an inopportune moment
        pass

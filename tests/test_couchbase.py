import os
import unittest

from couchbase.options import (QueryOptions)

from davidkhala.couchbase import Couchbase
from davidkhala.couchbase.capella.organization import Organization

secret = os.getenv("CAPELLA_API_SECRET")
class CapellaTestCase(unittest.TestCase):

    def test_list_org(self):
        org = Organization(secret)
        print(org.list())

class CouchbaseTestCase(unittest.TestCase):
    couchbase: Couchbase

    @classmethod
    def setUpClass(cls):
        cls.couchbase = Couchbase('couchbase', tls=False)
        cls.couchbase.connect('travel-sample')
        cls.cb_coll = cls.couchbase.bucket.scope("inventory").collection("airline")

    def test_upsert(self):

        def upsert_document(doc):
            """
            upsert document function
            """
            print("\nUpsert CAS: ")

            # key will equal: "airline_8091"
            key = doc["type"] + "_" + str(doc["id"])
            result = self.cb_coll.upsert(key, doc)
            print(result.cas)


        airline = {
            "type": "airline",
            "id": 8091,
            "callsign": "CBS",
            "iata": None,
            "icao": None,
            "name": "Couchbase Airways",
        }

        upsert_document(airline)
        self.lookup_by_callsign("CBS")

    def test_query(self):

        def get_airline_by_key(key):
            """
            get document function
            """
            print("\nGet Result: ")
            result = self.cb_coll.get(key)
            print(result.content_as[str])

        get_airline_by_key("airline_8091")

    def lookup_by_callsign(self,cs):
        print("\nLookup Result: ")

        inventory_scope = self.couchbase.bucket.scope('inventory')
        sql_query = 'SELECT VALUE name FROM airline WHERE callsign = $1'
        row_iter = inventory_scope.query(
            sql_query,
            QueryOptions(positional_parameters=[cs]))
        for row in row_iter:
            self.assertEqual("Couchbase Airways", row)
            print(row)




if __name__ == '__main__':
    unittest.main()

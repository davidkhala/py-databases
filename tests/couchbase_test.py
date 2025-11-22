import os
import unittest

from couchbase.collection import Collection
from couchbase.options import (QueryOptions)

from davidkhala.data.base.couchbase import Couchbase
from davidkhala.data.base.couchbase.capella.bucket import calculateId, Sample
from davidkhala.data.base.couchbase.capella.cluster import Cluster
from davidkhala.data.base.couchbase.capella.organization import Organization
from davidkhala.data.base.couchbase.capella.project import Project

secret = os.getenv("API_SECRET")
password = os.getenv("ADMINISTRATOR_PASSWORD")


class CapellaTestCase(unittest.TestCase):
    organization_id: str
    project_id: str
    cluster_id: str
    domain: str
    couchbase: Couchbase
    collection: Collection

    @classmethod
    def setUpClass(cls):
        org = Organization(secret)
        cls.organization_id = org.list()[0]['id']
        project = Project(secret, cls.organization_id)
        cls.project_id = project.list()[0]['id']
        cluster = Cluster(secret, cls.organization_id, cls.project_id)
        cls.cluster_id = cluster.list()[0]['id']
        operator = Cluster.Operator(secret, cls.organization_id, cls.project_id, cls.cluster_id)
        operator.ensure_started()
        sample = Sample(secret, cls.organization_id, cls.project_id, cls.cluster_id)
        list(sample.preset())
        cls.couchbase = Couchbase(password, domain=operator.domain)
        cls.couchbase.connect('travel-sample')
        cls.collection = cls.couchbase.bucket.scope("inventory").collection("airline")

    def test_dependencies(self):
        self.assertEqual('dHJhdmVsLXNhbXBsZQ==', calculateId('travel-sample'))

    def test_upsert(self):
        def upsert_document(doc):
            """
            upsert document function
            """
            print("\nUpsert CAS: ")

            # key will equal: "airline_8091"
            key = doc["type"] + "_" + str(doc["id"])
            result = self.collection.upsert(key, doc)
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
            result = self.collection.get(key)
            print(result.content_as[str])

        get_airline_by_key("airline_8091")

    def lookup_by_callsign(self, cs):
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

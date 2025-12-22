import os
import unittest

from couchbase.options import (QueryOptions)
from requests import HTTPError

from davidkhala.data.base.couchbase import Couchbase
from davidkhala.data.base.couchbase.capella.bucket import calculateId, Sample
from davidkhala.data.base.couchbase.capella.cluster import Cluster
from davidkhala.data.base.couchbase.capella.organization import Organization
from davidkhala.data.base.couchbase.capella.project import Project

secret = os.getenv("API_SECRET") or 'V0tDTlZFWTRKR0JaNG1ObW9WaWl3OXlOS1hpZnFOQ3o6Q1g0ZitLUVFaNmpjTFVvZV9JY2hIQiVFaGxGQERlNnVMT0pebngtMGhnSGglOD90YS1FcEZlZUpDSHB2JCViRA=='
password = os.getenv("ADMINISTRATOR_PASSWORD") or 'CouchBase-david@2025'


class CapellaTestCase(unittest.TestCase):

    def setUp(self):
        org = Organization(secret)
        self.organization_id = org.list()[0]['id']
        project = Project(secret, self.organization_id)
        self.project_id = project.list()[0]['id']
        cluster = Cluster(secret, self.organization_id, self.project_id)
        self.cluster_id = cluster.list()[0]['id']
        self.operator = Cluster.Operator(secret, self.organization_id, self.project_id, self.cluster_id)
        self.operator.ensure_started()
        sample = Sample(secret, self.organization_id, self.project_id, self.cluster_id)
        list(sample.preset())
        self.couchbase = Couchbase(password, domain=self.operator.domain)
        self.couchbase.bucket_name = 'travel-sample'
        self.couchbase.connect()
        self.collection = (self.couchbase.bucket.scope("inventory").collection("airline"))

    def test_dependencies(self):
        self.assertEqual('dHJhdmVsLXNhbXBsZQ==', calculateId('travel-sample'))

    def test_appService(self):
        operator = self.operator.appServiceOperator
        print(operator.get())
        if operator.is_free:
            with self.assertRaises(HTTPError) as e:
                operator.stop()
            self.assertEqual(e.exception.response.status_code, 422, 'This resource is not available during your self-service trial. Upgrade for access.')

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

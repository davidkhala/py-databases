import base64

from davidkhala.couchbase.capella.http import API


def calculateId(name: str) -> str:
    return base64.b64encode(name.encode('utf-8')).decode('utf-8')


class Sample:
    name = {
        'travel': 'travel-sample', 'game': 'gamesim-sample', 'beer': 'beer-sample'
    }
    def __init__(self, api_secret, organization_id, project_id, cluster_id):
        self.api = API(f"/${organization_id}/projects/${project_id}/clusters/${cluster_id}/sampleBuckets", api_secret)
        self.organization_id = organization_id
        self.project_id = project_id
        self.cluster_id = cluster_id

    def preset(self, *names):
        if len(names)==0:
            existing_names = self.existing()
            names = [s for s in Sample.name.values() if s not in existing_names]
        for name in names:
            yield self.load(name,10)

    def existing(self):
        return self.list().map(...)
    def list(self):
        return self.api.get()['data']
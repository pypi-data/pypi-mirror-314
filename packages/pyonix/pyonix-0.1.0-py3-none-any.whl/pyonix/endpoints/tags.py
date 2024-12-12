# ionix_api/endpoints/tags.py
from pyonix.client import IonixClient

class Tags:
    def __init__(self, client: IonixClient):
        self.client = client

    def post(self, ids=[], tags=[]):
        
        payload = {
            "ids": ids,
            "tags": tags
        }
        return self.client.post("discovery/org-assets/tags/?fields=id,risk_score,asset,type,importance,hosting_provider,technologies,first_seen,service_type,service,tags,groups", data=payload)


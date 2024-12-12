# ionix_api/endpoints/assessments.py
from pyonix.client import IonixClient

class Dashboards:
    def __init__(self, client: IonixClient):
        self.client = client

    def get(self, asset=None, limit=None, offset=None, **kwargs):
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return self.client.get("dashboard/summary/", params=params)


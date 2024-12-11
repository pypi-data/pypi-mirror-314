from django.conf import settings

from zs_utils.api.base_api import BaseAPI


class AmocrmAPI(BaseAPI):
    production_api_url = settings.AMOCRM_API_URL
    drop_empty_params = True

    def __init__(self, access_token: str, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

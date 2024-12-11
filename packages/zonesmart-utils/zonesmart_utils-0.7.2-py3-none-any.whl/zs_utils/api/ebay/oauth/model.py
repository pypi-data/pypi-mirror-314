from django.utils import timezone


class env_type:
    def __init__(self, config_id, web_endpoint, api_endpoint):
        self.config_id = config_id
        self.web_endpoint = web_endpoint
        self.api_endpoint = api_endpoint


class environment:
    PRODUCTION = env_type(
        "api.ebay.com",
        "https://auth.ebay.com/oauth2/authorize",
        "https://api.ebay.com/identity/v1/oauth2/token",
    )
    SANDBOX = env_type(
        "api.sandbox.ebay.com",
        "https://auth.sandbox.ebay.com/oauth2/authorize",
        "https://api.sandbox.ebay.com/identity/v1/oauth2/token",
    )


class oAuth_token:
    def __init__(
        self,
        error=None,
        access_token: str = None,
        refresh_token: str = None,
        expires_in: int = None,
        refresh_token_expires_in: int = None,
        token_type: str = None,
        **kwargs,
    ):
        """
        access_token_expiry: datetime in UTC
        refresh_token_expiry: datetime in UTC
        """

        self.error = error
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type

        now = timezone.now()

        if expires_in:
            self.access_token_expiry = now + timezone.timedelta(seconds=expires_in)
        else:
            self.access_token_expiry = None

        if refresh_token_expires_in:
            self.refresh_token_expiry = now + timezone.timedelta(seconds=refresh_token_expires_in)
        else:
            self.refresh_token_expiry = None

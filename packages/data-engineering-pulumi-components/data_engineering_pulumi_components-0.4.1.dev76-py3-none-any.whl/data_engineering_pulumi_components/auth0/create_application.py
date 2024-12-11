from typing import Optional
from pulumi import ComponentResource, ResourceOptions
from data_engineering_pulumi_components.utils import Tagger
import pulumi_auth0 as auth0
import pulumi_auth0.provider as provider


class Auth0PasswordLessClient(ComponentResource):
    def __init__(
        self,
        name: str,
        tagger: Tagger,
        auth0_domain: str,
        web_origin: str,
        client_id: str,
        client_secret: str,
        auth0_debug: str,
        application_url: str,
        add_local_host: bool,
        template: str = "",
        opts: Optional[ResourceOptions] = None,
    ) -> None:
        super().__init__(
            name=name,
            t="data-engineering-pulumi-components:aws:webapplication",
            opts=opts,
        )
        self._opts = opts
        self._name = name
        self._tagger = tagger

        # Create a tenant (area where all apis + apps are created) manually.
        # Create a machine-to-machine api manually and use its clientid + client secret
        # to create applications
        # create provider. using provider you can create app
        self._auth_provider = provider.Provider(
            resource_name=f"{name}-auth0-provider",
            opts=None,
            domain=auth0_domain,
            client_id=client_id,
            client_secret=client_secret,
            debug=auth0_debug,
        )
        self._client = auth0.Client(
            resource_name=f"{name}-web-application",
            app_type="regular_web",
            allowed_logout_urls=[
                "https://localhost:5000/start"
                if add_local_host
                else application_url + "/start",
            ],
            allowed_origins=[application_url],
            callbacks=[
                "https://localhost:5000/callback"
                if add_local_host
                else application_url + "/callback",
            ],
            client_secret_rotation_trigger={
                "triggered_at": "2018-01-02T23:12:01Z",
                "triggered_by": "auth0",
            },
            custom_login_page_on=True,
            description="Data engineering uploader",
            grant_types=[
                "authorization_code",
                "http://auth0.com/oauth/grant-type/password-realm",
                "implicit",
                "password",
                "refresh_token",
            ],
            initiate_login_uri=application_url + "/login",
            is_first_party=True,
            is_token_endpoint_ip_header_trusted=True,
            organization_require_behavior="no_prompt",
            organization_usage="deny",
            oidc_conformant=True,
            refresh_token=auth0.ClientRefreshTokenArgs(
                expiration_type="expiring",
                idle_token_lifetime=200,
                infinite_idle_token_lifetime=True,
                infinite_token_lifetime=False,
                leeway=15,
                rotation_type="rotating",
                token_lifetime=300,
            ),
            token_endpoint_auth_method="client_secret_post",
            web_origins=[
                "http://localhost:5000" if add_local_host else web_origin,
            ],
            jwt_configuration=auth0.GlobalClientJwtConfigurationArgs(alg="RS256"),
            opts=ResourceOptions(
                provider=self._auth_provider, depends_on=self._auth_provider
            ),
        )
        self._connection = auth0.Connection(
            "passwordlessEmail",
            show_as_button=True,
            is_domain_connection=False,
            options=auth0.ConnectionOptionsArgs(
                from_=f"{name}root@auth0.com",
                subject="Welcome to {{ application.name }}",
                syntax="liquid",
                template=template,
                brute_force_protection=True,
                scopes=["openid", "profile", "email"],
                debug=True,
                disable_cache=True,
                disable_signup=True,
                import_mode=False,
                totp=auth0.ConnectionOptionsTotpArgs(time_step=300, length=6),
                name="email",
                tenant_domain=auth0_domain,
                enabled_database_customization=False,
            ),
            strategy="email",
            display_name="Passwordless Connection",
            opts=ResourceOptions(
                provider=self._auth_provider, depends_on=self._auth_provider
            ),
        )

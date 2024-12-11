"""context.py"""

import os

from fastapi import Request
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from sw_product_lib import DEFAULT_PLATFORM_BASE_URL, in_dev_mode
from sw_product_lib.apps.auth import gcp, sw_proxy
from sw_product_lib.platform.gql import ProductAPI


class AppContext(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    product_slug: str | None = Field(
        default=None, alias=AliasChoices("product_slug", "ProductSlug")
    )
    product_api_key: str | None = os.environ.get("PRODUCT_LIB_API_KEY")
    base_url: str = os.environ.get("PRODUCT_LIB_BASE_URL", DEFAULT_PLATFORM_BASE_URL)
    api: ProductAPI | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.api is None and self.product_api_key:
            self.api = ProductAPI(api_key=self.product_api_key, base_url=self.base_url)


class SchedulerRequestContext(AppContext):
    """Context for Scheduler Requests.

    Expects a JWT token from a Google Cloud service account.
    """

    scheduler_jwt: str | None = None
    claims: dict | None = None

    @classmethod
    def from_request(cls, request: Request):
        claims, token = gcp.verify_token(
            request=request, verify_signature=not in_dev_mode()
        )

        return cls(scheduler_jwt=token, claims=claims)


class UserRequestContext(AppContext):
    """Context for User-Initiated Requests.

    Expects a Strangeworks platform proxy jwt token.
    """

    workspace_member_slug: str = Field(
        alias=AliasChoices("workspace_member_slug", "WorkspaceMemberSlug")
    )
    resource_slug: str = Field(
        default=None, alias=AliasChoices("resource_slug", "ResourceSlug")
    )
    resource_token_id: str | None = Field(
        default=None, alias=AliasChoices("resource_token_id", "ResourceTokenID")
    )
    resource_entitlements: list[str] | None = Field(
        default=None, alias=AliasChoices("ResourceEntitlements")
    )
    workspace_slug: str | None = Field(
        default=None, alias=AliasChoices("workspace_slug", "WorkspaceSlug")
    )

    parent_job_slug: str | None = None
    experiment_trial_id: str | None = None

    proxy_jwt: str | None = Field(
        default=None,
        alias=AliasChoices("_auth_token", "proxy_jwt", "x-strangeworks-access-token"),
    )

    @classmethod
    def from_request(cls, request: Request):
        claims, token = sw_proxy.verify_token(
            request=request, verify_signature=not in_dev_mode()
        )
        return cls(
            proxy_jwt=token,
            parent_job_slug=request.headers.get("x-strangeworks-parent-job-slug"),
            experiment_trial_id=request.headers.get(
                "x-strangeworks-experiment-trial-id"
            ),
            **claims
        )

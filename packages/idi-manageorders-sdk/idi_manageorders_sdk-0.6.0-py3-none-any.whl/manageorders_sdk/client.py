"""Interacting with ManageOrders API."""

from datetime import UTC, datetime, timedelta
from typing import Any, Self

import httpx
from httpx import Response

from .models import Order


class ManageOrdersClient:
    """A class wrapping interaction with ManageOrders API."""

    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        """Initialize the ManageOrdersClient class."""
        self.base_url = "https://manageordersapi.com"
        self.username = username
        self.password = password
        self.token = ""
        self.token_expires_at = datetime.now(tz=UTC)

    def _update_token(self: Self) -> None:
        """Update the OAUTH token."""
        if self.token_expires_at > datetime.now(tz=UTC):
            return

        auth_dict = {
            "username": self.username,
            "password": self.password,
        }
        response = httpx.post(f"{self.base_url}/v1/manageorders/signin", json=auth_dict)
        response.raise_for_status()
        data = response.json()
        self.token = data["id_token"]
        self.token_expires_at = datetime.now(tz=UTC) + timedelta(hours=1)

    def _make_request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Response:
        """Make a request to Core."""
        self._update_token()

        headers = {"Authorization": "Bearer " + self.token}

        args = {
            "url": self.base_url + path,
            "method": method,
            "headers": headers,
        }

        if params is not None:
            args["params"] = params

        if json is not None:
            args["json"] = json

        return httpx.request(**args)  # type: ignore[arg-type]

    def upload_order(
        self,
        order: Order,
    ) -> Response:
        """Upload an order to ManageOrders."""
        return self._make_request("POST", "/onsite/order-push", json=order.model_dump(by_alias=True, exclude_none=True))

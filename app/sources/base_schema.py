import asyncio
import httpx

from fastapi import HTTPException
from pydantic import BaseModel

from app.core.config import settings


class SourceBase(BaseModel):
    name: str
    base_url: str
    subscription_url: str
    data_fetch_url: str
    topics: str
    description: str

    async def subscribe(self, user_id: str, webhook_postfix: str, max_retries: int = 3, backoff: float = 2.0):
        url = self.base_url + self.subscription_url
        retries = 0
        while retries < max_retries:
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.post(
                        url.format(stream=user_id), json={'endpoint': settings.USER_SUB_WEBHOOK + webhook_postfix}
                    )
                    response.raise_for_status()

                return response

            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                retries += 1
                if retries >= max_retries:
                    raise HTTPException(
                        status_code=503,
                        detail=f"Failed to subscribe after {max_retries} attempts: {exc}"
                    )

                await asyncio.sleep(backoff * (2 ** (retries - 1)))

    async def unsubscribe(self, user_id: str, max_retries: int = 3, backoff: float = 2.0):
        url = self.base_url + self.subscription_url
        retries = 0

        while retries < max_retries:
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.post(
                        url.format(stream=user_id), json={'endpoint': None}
                    )
                    response.raise_for_status()

                return response

            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                retries += 1
                if retries >= max_retries:
                    raise HTTPException(
                        status_code=503,
                        detail=f"Failed to subscribe after {max_retries} attempts: {exc}"
                    )

                await asyncio.sleep(backoff * (2 ** (retries - 1)))

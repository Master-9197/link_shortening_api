from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from pydantic import AnyUrl
import jwt

from ..schemas.links import ShortLink
from ..services.auth import config
from ..services.link_shortening import LinkShorteningService


router = APIRouter(
    tags=["Сокращение ссылок"]
)


async def get_current_user(requests: Request):
    jwt_token = requests.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        paload: dict = jwt.decode(jwt_token, key=config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
        return paload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invailid token")


@router.post("/api/short")
async def short_link(
        url: AnyUrl,
        user_id: int = Depends(get_current_user)
    ) -> ShortLink:

    link = await LinkShorteningService.short_link(url=str(url), user_id=user_id)
    return {"short_link": link}


@router.get("/{link_hash}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_user(link_hash: str) -> RedirectResponse:
    url = await LinkShorteningService.get_link_from_hash(hash=link_hash)
    return RedirectResponse(url)
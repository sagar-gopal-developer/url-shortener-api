from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_short_url
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/shorten",
    response_model=URLResponse
)
def shorten_url(
    url: URLCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_short_url(
        db=db,
        url=url,
        user_id=current_user.id
    )
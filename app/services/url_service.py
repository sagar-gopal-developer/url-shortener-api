from sqlalchemy.orm import Session

from app.models.url import URL
from app.schemas.url import URLCreate
from app.utils.shortener import generate_short_code


def create_short_url(
    db: Session,
    url: URLCreate,
    user_id: int
):
    short_code = generate_short_code()

    new_url = URL(
        original_url=url.original_url,
        short_code=short_code,
        clicks=0,
        user_id=user_id
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url
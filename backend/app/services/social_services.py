from app.models.user import SocialAccount
from datetime import datetime

async def save_social_account(user_id: int, platform: str, username: str, profile_url: str, avatar_url: str):
    existing = await SocialAccount.get_or_none(user_id=user_id, platform=platform)

    if existing:
        existing.username = username
        existing.profile_url = profile_url
        existing.avatar_url = avatar_url
        existing.last_checked = datetime.utcnow()
        await existing.save()
    else:
        await SocialAccount.create(
            user_id=user_id,
            platform=platform,
            username=username,
            profile_url=profile_url,
            avatar_url=avatar_url,
            connected_at=datetime.utcnow(),
            last_checked=datetime.utcnow()
        )

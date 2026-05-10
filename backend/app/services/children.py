from __future__ import annotations

from collections.abc import Mapping

from app.db.postgres import get_db_connection


async def get_child_for_user(child_id: str, user_id: str) -> Mapping[str, object] | None:
    """Return a child row owned by the given user, or None."""
    async with get_db_connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                select
                    id::text as id,
                    user_id::text as user_id,
                    name,
                    age,
                    personality,
                    favorite_character,
                    created_at,
                    updated_at
                from public.children
                where id = %s::uuid
                  and user_id = %s::uuid
                limit 1
                """,
                (child_id, user_id),
            )
            return await cursor.fetchone()

from typing import Optional
from datetime import datetime, timezone

from sqlalchemy.types import TypeDecorator, DateTime


class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: Optional[datetime], dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("Expects aware datetime")
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value: Optional[datetime], dialect):
        if value is None:
            return None
        return value.replace(tzinfo=timezone.utc)
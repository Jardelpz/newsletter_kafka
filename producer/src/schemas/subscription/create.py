import datetime

from pydantic import BaseModel, validator
from typing import Optional


class Subscription(BaseModel):
    name: str
    email: str
    age: int
    genre: str
    subscription_date: Optional[str]

    @validator('subscription_date', pre=True, always=True)
    def set_subscription_date(cls, subscription_date):
        return subscription_date or datetime.datetime.now().isoformat()

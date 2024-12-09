from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional


class DeliveryPeriodReadView(BaseModel):
    _from: Optional[str] = None
    delivery_period_pub_id: Optional[str] = None
    is_deletable: Optional[str] = None
    is_editable: Optional[str] = None
    address_pub_id: Optional[str] = None
    to: Optional[str] = None


DeliveryPeriodReadView.model_rebuild()

from typing import Optional
from sqlmodel import Field, SQLModel

class WalletModel(SQLModel, table=True):
    __tablename__: str = 'wallet'

    id: int = Field(primary_key=True)
    name: str
    description: str
    user_id: int
# PortfolioModel.py

from pydantic import BaseModel

class PortfolioModel(BaseModel):
    title: str
    description: str
    user_id: int

# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from PortfolioModel import SessionLocal, Portfolio

# FastAPI setup
app = FastAPI()


# Pydantic model for request/response
class PortfolioModel(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True  # Allow Pydantic to read data from SQLAlchemy models


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/portfolios", response_model=List[PortfolioModel])
async def read_portfolios(db: Session = Depends(get_db)):
    portfolios = db.query(Portfolio).all()  # Retrieve all portfolios from the database
    return portfolios


@app.post("/portfolios", response_model=PortfolioModel)
async def create_portfolio(portfolio: PortfolioModel, db: Session = Depends(get_db)):
    db_portfolio = Portfolio(**portfolio.dict())
    db.add(db_portfolio)  # Add portfolio to the session
    db.commit()  # Commit the session to save the portfolio to the database
    db.refresh(db_portfolio)  # Refresh the instance to get the updated data (like ID)
    return db_portfolio


@app.put("/portfolios/{portfolio_id}", response_model=PortfolioModel)
async def update_portfolio(portfolio_id: int, portfolio: PortfolioModel, db: Session = Depends(get_db)):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    for key, value in portfolio.dict().items():
        setattr(db_portfolio, key, value)  # Update fields
    db.commit()  # Commit the changes to the database
    return db_portfolio


@app.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(db_portfolio)  # Delete portfolio from the session
    db.commit()  # Commit the changes to the database
    return {"message": "Portfolio deleted"}

# Run the application with: uvicorn main:app --reload

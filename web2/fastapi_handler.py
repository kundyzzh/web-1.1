# main.py
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from PortfolioModel import SessionLocal, Portfolio
import os

# FastAPI setup
app = FastAPI()

# File upload directory
UPLOAD_DIRECTORY = "./uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Create directory if it doesn't exist


# Pydantic model for request/response
class PortfolioModel(BaseModel):
    id: int
    user_id: int  # User ID
    name: str
    description: str
    file_path: str  # Path to the uploaded file

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
async def create_portfolio(user_id: int, name: str, description: str, file: UploadFile = File(...),
                           db: Session = Depends(get_db)):
    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    # Create the portfolio instance with the uploaded file's path
    db_portfolio = Portfolio(user_id=user_id, name=name, description=description, file_path=file_location)
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

from fastapi import FastAPI, HTTPException, Depends, Form, Request
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from PortfolioModel import SessionLocal, Portfolio
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Pydantic model for request/response
class PortfolioModel(BaseModel):
    id: int = None
    name: str
    description: str

    class Config:
        orm_mode = True

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/portfolios", response_class=HTMLResponse)
async def get_portfolio(request: Request, db: Session = Depends(get_db)):
    portfolios = db.query(Portfolio).all()
    return templates.TemplateResponse("portfolio.html", {"request": request, "portfolios": portfolios})

@app.post("/portfolios", response_class=HTMLResponse)
async def create_portfolio(
        request: Request,  # Move request here
        name: str = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db)
):
    db_portfolio = Portfolio(name=name, description=description)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)

    # Fetch all portfolios after adding the new one
    portfolios = db.query(Portfolio).all()

    # Return the updated portfolio page
    return templates.TemplateResponse("portfolio.html", {"request": request, "portfolios": portfolios})

@app.put("/portfolios/{portfolio_id}", response_model=PortfolioModel)
async def update_portfolio(portfolio_id: int, portfolio: PortfolioModel, db: Session = Depends(get_db)):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    for key, value in portfolio.dict().items():
        setattr(db_portfolio, key, value)
    db.commit()
    return db_portfolio

@app.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(db_portfolio)
    db.commit()
    return {"message": "Portfolio deleted"}

# Run the application with: uvicorn main:app --reload

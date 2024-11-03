# fastapi_app.py

from fastapi import FastAPI
from typing import List
from PortfolioModel import PortfolioModel

app = FastAPI()
portfolios = []

@app.get("/portfolios", response_model=List[PortfolioModel])
async def read_portfolios():
    return portfolios

@app.post("/portfolios", response_model=PortfolioModel)
async def create_portfolio(portfolio: PortfolioModel):
    portfolios.append(portfolio)  # Adds the portfolio to the list.
    return portfolio

@app.put("/portfolios/{portfolio_id}", response_model=PortfolioModel)
async def update_portfolio(portfolio_id: int, portfolio: PortfolioModel):
    portfolios[portfolio_id] = portfolio  # Updates the portfolio in the list.
    return portfolio

@app.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: int):
    del portfolios[portfolio_id]  # Deletes the portfolio from the list.
    return {"message": "Portfolio deleted"}  # Returns an informative message.

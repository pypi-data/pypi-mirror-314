from datetime import datetime
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel

def test_balance_sheet_models(session):
    # Test annual balance sheet
    annual_bs = AnnualBalanceSheetStatementModel(
        symbol="AAPL",
        fiscal_date_ending=datetime(2023, 12, 31),
        reported_currency="USD",
        total_assets=1000000.0,
        total_current_assets=500000.0,
        cash_and_cash_equivalents=200000.0,
        total_liabilities=600000.0,
        total_stockholders_equity=400000.0
    )
    
    session.add(annual_bs)
    session.commit()
    
    result = session.query(AnnualBalanceSheetStatementModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert result.total_assets == 1000000.0
    assert result.total_stockholders_equity == 400000.0

def test_income_statement_models(session):
    # Test quarterly income statement
    quarter_is = QuarterlyIncomeStatementModel(
        symbol="AAPL",
        fiscal_date_ending=datetime(2023, 3, 31),
        reported_currency="USD",
        revenue=100000.0,
        gross_profit=40000.0,
        net_income=20000.0,
        ebitda=30000.0,
        eps=2.5,
        eps_diluted=2.4
    )
    
    session.add(quarter_is)
    session.commit()
    
    result = session.query(QuarterlyIncomeStatementModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert result.revenue == 100000.0
    assert result.eps == 2.5

def test_cashflow_statement_models(session):
    # Test annual cashflow statement
    annual_cf = AnnualCashFlowStatementModel(
        symbol="AAPL",
        fiscal_date_ending=datetime(2023, 12, 31),
        reported_currency="USD",
        operating_cash_flow=50000.0,
        capital_expenditure=-10000.0,
        free_cash_flow=40000.0,
        net_income=20000.0,
        depreciation_and_amortization=5000.0
    )
    
    session.add(annual_cf)
    session.commit()
    
    result = session.query(AnnualCashFlowStatementModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert result.operating_cash_flow == 50000.0
    assert result.free_cash_flow == 40000.0 

def test_financial_ratios(session):
    # Test financial ratios and calculations
    balance_sheet = AnnualBalanceSheetStatementModel(
        symbol="AAPL",
        fiscal_date_ending=datetime(2023, 12, 31),
        reported_currency="USD",
        total_assets=1000000.0,
        total_current_assets=500000.0,
        cash_and_cash_equivalents=200000.0,
        total_liabilities=600000.0,
        total_stockholders_equity=400000.0
    )
    
    session.add(balance_sheet)
    session.commit()
    
    result = session.query(AnnualBalanceSheetStatementModel).first()
    
    # Calculate and test financial ratios
    current_ratio = result.total_current_assets / result.total_liabilities
    debt_to_equity = result.total_liabilities / result.total_stockholders_equity
    
    assert current_ratio > 0
    assert debt_to_equity > 0
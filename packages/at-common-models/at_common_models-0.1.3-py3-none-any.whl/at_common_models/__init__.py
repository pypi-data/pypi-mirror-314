# Import all models to register them with SQLAlchemy
from at_common_models.stock.overview import OverviewModel
from at_common_models.stock.daily_candlestick import DailyCandlestickModel
from at_common_models.stock.daily_indicator import DailyIndicatorModel
from at_common_models.stock.quotation import QuotationModel
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from at_common_models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from at_common_models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from at_common_models.news.article import NewsArticleModel
from at_common_models.news.stock import NewsStockModel

# These imports will register all models with the Base.metadata
__all__ = [
    'OverviewModel',
    'DailyCandlestickModel',
    'DailyIndicatorModel',
    'QuotationModel',
    'AnnualBalanceSheetStatementModel',
    'QuarterBalanceSheetStatementModel',
    'AnnualIncomeStatementModel',
    'QuarterlyIncomeStatementModel',
    'AnnualCashFlowStatementModel',
    'QuarterCashflowStatementModel',
    'NewsArticleModel',
    'NewsStockModel'
]

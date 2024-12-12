from sqlalchemy import Column, String, DateTime, DOUBLE
from at_common_models.base import Base

class BaseCashflowStatementModel(Base):
    """Base model for cash flow statements (both annual and quarter)"""
    __abstract__ = True

    # Primary identifiers
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    fiscal_date_ending = Column(DateTime, primary_key=True, nullable=False, index=True)
    reported_currency = Column(String(3), nullable=False)

    # Operating Activities - Core Operations
    net_income = Column(DOUBLE, nullable=False, default=0.0)
    depreciation_and_amortization = Column(DOUBLE, nullable=False, default=0.0)
    deferred_income_tax = Column(DOUBLE, nullable=False, default=0.0)
    stock_based_compensation = Column(DOUBLE, nullable=False, default=0.0)

    # Operating Activities - Working Capital Changes
    change_in_working_capital = Column(DOUBLE, nullable=False, default=0.0)
    accounts_receivables = Column(DOUBLE, nullable=False, default=0.0)
    inventory = Column(DOUBLE, nullable=False, default=0.0)
    accounts_payables = Column(DOUBLE, nullable=False, default=0.0)
    other_working_capital = Column(DOUBLE, nullable=False, default=0.0)
    other_non_cash_items = Column(DOUBLE, nullable=False, default=0.0)
    net_cash_provided_by_operating_activities = Column(DOUBLE, nullable=False, default=0.0)

    # Investing Activities
    investments_in_property_plant_and_equipment = Column(DOUBLE, nullable=False, default=0.0)
    acquisitions_net = Column(DOUBLE, nullable=False, default=0.0)
    purchases_of_investments = Column(DOUBLE, nullable=False, default=0.0)
    sales_maturities_of_investments = Column(DOUBLE, nullable=False, default=0.0)
    other_investing_activities = Column(DOUBLE, nullable=False, default=0.0)
    net_cash_used_for_investing_activities = Column(DOUBLE, nullable=False, default=0.0)

    # Financing Activities
    debt_repayment = Column(DOUBLE, nullable=False, default=0.0)
    common_stock_issued = Column(DOUBLE, nullable=False, default=0.0)
    common_stock_repurchased = Column(DOUBLE, nullable=False, default=0.0)
    dividends_paid = Column(DOUBLE, nullable=False, default=0.0)
    other_financing_activities = Column(DOUBLE, nullable=False, default=0.0)
    net_cash_used_provided_by_financing_activities = Column(DOUBLE, nullable=False, default=0.0)

    # Cash Position and Summary Metrics
    effect_of_forex_changes_on_cash = Column(DOUBLE, nullable=False, default=0.0)
    net_change_in_cash = Column(DOUBLE, nullable=False, default=0.0)
    cash_at_end_of_period = Column(DOUBLE, nullable=False, default=0.0)
    cash_at_beginning_of_period = Column(DOUBLE, nullable=False, default=0.0)
    operating_cash_flow = Column(DOUBLE, nullable=False, default=0.0)
    capital_expenditure = Column(DOUBLE, nullable=False, default=0.0)
    free_cash_flow = Column(DOUBLE, nullable=False, default=0.0)

    def __str__(self):
        return f"<{self.__class__.__name__}(symbol={self.symbol}, fiscal_date_ending={self.fiscal_date_ending})>"

    def __repr__(self):
        return self.__str__()

class BaseBalanceSheetStatementModel(Base):
    """Base model for balance sheet statements (both annual and quarter)"""
    __abstract__ = True

    # Primary identifiers
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    fiscal_date_ending = Column(DateTime, primary_key=True, nullable=False, index=True)
    reported_currency = Column(String(3), nullable=False)

    # Current Assets
    cash_and_cash_equivalents = Column(DOUBLE, nullable=False, default=0.0)
    short_term_investments = Column(DOUBLE, nullable=False, default=0.0)
    cash_and_short_term_investments = Column(DOUBLE, nullable=False, default=0.0)
    net_receivables = Column(DOUBLE, nullable=False, default=0.0)
    inventory = Column(DOUBLE, nullable=False, default=0.0)
    other_current_assets = Column(DOUBLE, nullable=False, default=0.0)
    total_current_assets = Column(DOUBLE, nullable=False, default=0.0)

    # Non-Current Assets
    property_plant_equipment_net = Column(DOUBLE, nullable=False, default=0.0)
    goodwill = Column(DOUBLE, nullable=False, default=0.0)
    intangible_assets = Column(DOUBLE, nullable=False, default=0.0)
    goodwill_and_intangible_assets = Column(DOUBLE, nullable=False, default=0.0)
    long_term_investments = Column(DOUBLE, nullable=False, default=0.0)
    tax_assets = Column(DOUBLE, nullable=False, default=0.0)
    other_non_current_assets = Column(DOUBLE, nullable=False, default=0.0)
    total_non_current_assets = Column(DOUBLE, nullable=False, default=0.0)

    # Asset Totals
    other_assets = Column(DOUBLE, nullable=False, default=0.0)
    total_assets = Column(DOUBLE, nullable=False, default=0.0)

    # Current Liabilities
    account_payables = Column(DOUBLE, nullable=False, default=0.0)
    short_term_debt = Column(DOUBLE, nullable=False, default=0.0)
    tax_payables = Column(DOUBLE, nullable=False, default=0.0)
    deferred_revenue = Column(DOUBLE, nullable=False, default=0.0)
    other_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)
    total_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)

    # Non-Current Liabilities
    long_term_debt = Column(DOUBLE, nullable=False, default=0.0)
    deferred_revenue_non_current = Column(DOUBLE, nullable=False, default=0.0)
    deferred_tax_liabilities_non_current = Column(DOUBLE, nullable=False, default=0.0)
    other_non_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)
    total_non_current_liabilities = Column(DOUBLE, nullable=False, default=0.0)

    # Liability Totals
    other_liabilities = Column(DOUBLE, nullable=False, default=0.0)
    capital_lease_obligations = Column(DOUBLE, nullable=False, default=0.0)
    total_liabilities = Column(DOUBLE, nullable=False, default=0.0)

    # Stockholders' Equity
    preferred_stock = Column(DOUBLE, nullable=False, default=0.0)
    common_stock = Column(DOUBLE, nullable=False, default=0.0)
    retained_earnings = Column(DOUBLE, nullable=False, default=0.0)
    accumulated_other_comprehensive_income_loss = Column(DOUBLE, nullable=False, default=0.0)
    other_total_stockholders_equity = Column(DOUBLE, nullable=False, default=0.0)
    total_stockholders_equity = Column(DOUBLE, nullable=False, default=0.0)
    total_equity = Column(DOUBLE, nullable=False, default=0.0)

    # Balance Sheet Totals
    total_liabilities_and_stockholders_equity = Column(DOUBLE, nullable=False, default=0.0)
    minority_interest = Column(DOUBLE, nullable=False, default=0.0)
    total_liabilities_and_total_equity = Column(DOUBLE, nullable=False, default=0.0)

    # Additional Financial Metrics
    total_investments = Column(DOUBLE, nullable=False, default=0.0)
    total_debt = Column(DOUBLE, nullable=False, default=0.0)
    net_debt = Column(DOUBLE, nullable=False, default=0.0)

    def __str__(self):
        return f"<{self.__class__.__name__}(symbol={self.symbol}, fiscal_date_ending={self.fiscal_date_ending})>"

    def __repr__(self):
        return self.__str__()

class BaseIncomeStatementModel(Base):
    """Base model for income statements (both annual and quarter)"""
    __abstract__ = True

    # Identifying information
    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    fiscal_date_ending = Column(DateTime, primary_key=True, nullable=False, index=True)
    reported_currency = Column(String(3), nullable=False)

    # Revenue and direct costs
    revenue = Column(DOUBLE, nullable=False, default=0.0)
    cost_of_revenue = Column(DOUBLE, nullable=False, default=0.0)
    gross_profit = Column(DOUBLE, nullable=False, default=0.0)
    gross_profit_ratio = Column(DOUBLE, nullable=False, default=0.0)

    # Operating expenses breakdown
    research_and_development_expenses = Column(DOUBLE, nullable=False, default=0.0)
    general_and_administrative_expenses = Column(DOUBLE, nullable=False, default=0.0)
    selling_and_marketing_expenses = Column(DOUBLE, nullable=False, default=0.0)
    selling_general_and_administrative_expenses = Column(DOUBLE, nullable=False, default=0.0)
    other_expenses = Column(DOUBLE, nullable=False, default=0.0)
    operating_expenses = Column(DOUBLE, nullable=False, default=0.0)
    cost_and_expenses = Column(DOUBLE, nullable=False, default=0.0)

    # Interest and depreciation
    interest_income = Column(DOUBLE, nullable=False, default=0.0)
    interest_expense = Column(DOUBLE, nullable=False, default=0.0)
    depreciation_and_amortization = Column(DOUBLE, nullable=False, default=0.0)

    # Profitability metrics
    ebitda = Column(DOUBLE, nullable=False, default=0.0)
    operating_income = Column(DOUBLE, nullable=False, default=0.0)
    total_other_income_expenses_net = Column(DOUBLE, nullable=False, default=0.0)
    income_before_tax = Column(DOUBLE, nullable=False, default=0.0)
    income_tax_expense = Column(DOUBLE, nullable=False, default=0.0)
    net_income = Column(DOUBLE, nullable=False, default=0.0)

    # Per share metrics
    eps = Column(DOUBLE, nullable=False, default=0.0)
    eps_diluted = Column(DOUBLE, nullable=False, default=0.0)

    def __str__(self):
        return f"<{self.__class__.__name__}(symbol={self.symbol}, fiscal_date_ending={self.fiscal_date_ending})>"

    def __repr__(self):
        return self.__str__()
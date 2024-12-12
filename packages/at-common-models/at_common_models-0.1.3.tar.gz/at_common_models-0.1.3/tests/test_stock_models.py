from datetime import datetime
from decimal import Decimal
from at_common_models.stock.overview import OverviewModel
from at_common_models.stock.quotation import QuotationModel
from at_common_models.stock.daily_candlestick import DailyCandlestickModel
from at_common_models.stock.daily_indicator import DailyIndicatorModel

def test_overview_model(session):
    # Create test data
    overview = OverviewModel(
        symbol="AAPL",
        exchange="NASDAQ",
        name="Apple Inc.",
        description="Technology company",
        currency="USD",
        country="USA",
        address="One Apple Park Way, Cupertino, CA",
        sector="Technology",
        industry="Consumer Electronics",
        ceo="Tim Cook",
        ipo_date=datetime(1980, 12, 12),
        modified_at=datetime.now()
    )
    
    # Test database operations
    session.add(overview)
    session.commit()
    
    # Query and verify
    result = session.query(OverviewModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert result.name == "Apple Inc."
    assert result.currency == "USD"

def test_quotation_model(session):
    # Create test data
    quotation = QuotationModel(
        symbol="AAPL",
        price=150.0,
        volume=1000000,
        previous_close=149.0,
        change=1.0,
        change_percentage=0.67,
        day_low=148.0,
        day_high=151.0,
        share_outstanding=16000000000,
        pe=25.5,
        timestamp=datetime.now()
    )
    
    session.add(quotation)
    session.commit()
    
    result = session.query(QuotationModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert result.price == 150.0
    assert result.volume == 1000000

def test_daily_candlestick_model(session):
    # Create test data
    candlestick = DailyCandlestickModel(
        symbol="AAPL",
        time=datetime.now(),
        open=Decimal("150.000"),
        high=Decimal("155.000"),
        low=Decimal("149.000"),
        close=Decimal("152.000"),
        volume=1000000
    )
    
    session.add(candlestick)
    session.commit()
    
    result = session.query(DailyCandlestickModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert float(result.open) == 150.0
    assert float(result.close) == 152.0

def test_daily_indicator_model(session):
    # Create test data
    indicator = DailyIndicatorModel(
        symbol="AAPL",
        time=datetime.now(),
        sma5=Decimal("150.000"),
        sma10=Decimal("149.000"),
        sma20=Decimal("148.000"),
        ema5=Decimal("150.500"),
        ema10=Decimal("149.500"),
        ema20=Decimal("148.500"),
        rsi=Decimal("65.000"),
        macd=Decimal("2.000"),
        macd_signal=Decimal("1.500"),
        macd_hist=Decimal("0.500"),
        slowk=Decimal("70.000"),
        slowd=Decimal("65.000"),
        upper_band=Decimal("155.000"),
        middle_band=Decimal("150.000"),
        lower_band=Decimal("145.000"),
        obv=1000000,
        roc=Decimal("2.500"),
        willr=Decimal("-30.000"),
        atr=Decimal("3.000"),
        sig_ma_cross_5_10=1,
        sig_ma_cross_10_20=0,
        sig_rsi_overbought=0,
        sig_rsi_oversold=0,
        sig_macd_crossover=1,
        sig_stoch_crossover=0,
        sig_bb_breakout_up=0,
        sig_bb_breakout_down=0,
        sig_volume_spike=1,
        sig_higher_high=1,
        sig_lower_low=0
    )
    
    session.add(indicator)
    session.commit()
    
    result = session.query(DailyIndicatorModel).filter_by(symbol="AAPL").first()
    assert result.symbol == "AAPL"
    assert float(result.rsi) == 65.0
    assert result.sig_ma_cross_5_10 == 1 

def test_overview_model_edge_cases(session):
    # Test with maximum length strings
    overview = OverviewModel(
        symbol="AAPL" * 10,  # Test long symbol
        exchange="NASDAQ",
        name="A" * 255,  # Test max length name
        description="D" * 1000,  # Test long description
        currency="USD",
        country="USA",
        address="A" * 500,  # Test long address
        sector="Technology",
        industry="Consumer Electronics",
        ceo="T" * 100,  # Test long CEO name
        ipo_date=datetime(1980, 12, 12),
        modified_at=datetime.now()
    )
    
    session.add(overview)
    session.commit()
    
    result = session.query(OverviewModel).first()
    assert len(result.symbol) <= 40
    assert len(result.name) <= 255
    assert len(result.description) <= 1000

def test_quotation_model_negative_values(session):
    # Test with negative values
    quotation = QuotationModel(
        symbol="AAPL",
        price=-150.0,  # Negative price
        volume=-1000000,  # Negative volume
        previous_close=-149.0,
        change=-1.0,
        change_percentage=-0.67,
        day_low=-148.0,
        day_high=-151.0,
        share_outstanding=-16000000000,
        pe=-25.5,
        timestamp=datetime.now()
    )
    
    session.add(quotation)
    session.commit()
    
    result = session.query(QuotationModel).first()
    assert result.price < 0
    assert result.volume < 0
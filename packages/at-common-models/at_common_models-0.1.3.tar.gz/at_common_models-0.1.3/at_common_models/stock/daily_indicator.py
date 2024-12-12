from sqlalchemy import Column, String, DateTime, DECIMAL, INTEGER, BIGINT
from at_common_models.base import Base

class DailyIndicatorModel(Base):
    __tablename__ = "stock_daily_indicators"

    symbol = Column(String(32), primary_key=True, nullable=False, index=True)
    time = Column(DateTime, primary_key=True, nullable=False, index=True)
    sma5 = Column(DECIMAL(10, 3), nullable=False)
    sma10 = Column(DECIMAL(10, 3), nullable=False)
    sma20 = Column(DECIMAL(10, 3), nullable=False)
    ema5 = Column(DECIMAL(10, 3), nullable=False)
    ema10 = Column(DECIMAL(10, 3), nullable=False)
    ema20 = Column(DECIMAL(10, 3), nullable=False)
    rsi = Column(DECIMAL(10, 3), nullable=False)
    macd = Column(DECIMAL(10, 3), nullable=False)
    macd_signal = Column(DECIMAL(10, 3), nullable=False)
    macd_hist = Column(DECIMAL(10, 3), nullable=False)
    slowk = Column(DECIMAL(10, 3), nullable=False)
    slowd = Column(DECIMAL(10, 3), nullable=False)
    upper_band = Column(DECIMAL(10, 3), nullable=False)
    middle_band = Column(DECIMAL(10, 3), nullable=False)
    lower_band = Column(DECIMAL(10, 3), nullable=False)
    obv = Column(BIGINT, nullable=False)
    roc = Column(DECIMAL(10, 3), nullable=False)
    willr = Column(DECIMAL(10, 3), nullable=False)
    atr = Column(DECIMAL(10, 3), nullable=False)
    sig_ma_cross_5_10 = Column(INTEGER, nullable=False)
    sig_ma_cross_10_20 = Column(INTEGER, nullable=False)
    sig_rsi_overbought = Column(INTEGER, nullable=False)
    sig_rsi_oversold = Column(INTEGER, nullable=False)
    sig_macd_crossover = Column(INTEGER, nullable=False)
    sig_stoch_crossover = Column(INTEGER, nullable=False)
    sig_bb_breakout_up = Column(INTEGER, nullable=False)
    sig_bb_breakout_down = Column(INTEGER, nullable=False)
    sig_volume_spike = Column(INTEGER, nullable=False)
    sig_higher_high = Column(INTEGER, nullable=False)
    sig_lower_low = Column(INTEGER, nullable=False)

    def __str__(self):
        return f"<DailyIndicatorModel(symbol={self.symbol}, time={self.time})>"

    def __repr__(self):
        return f"<DailyIndicatorModel(symbol={self.symbol}, time={self.time}>"
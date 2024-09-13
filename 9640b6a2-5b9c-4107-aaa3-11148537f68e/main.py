from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers we're interested in (in this case, just AAPL)
        self.tickers = ["AAPL"]
    
    @property
    def assets(self):
        # Return the list of tickers
        return self.tickers

    @property
    def interval(self):
        # Use daily interval for the strategy
        return "1day"

    def run(self, data):
        # Initialize variable for AAPL stake
        aapl_stake = 0
        # Calculate the short and long EMAs for AAPL
        short_ema = EMA("AAPL", data["ohlcv"], length=12)  # shorter EMA (e.g., 12 days)
        long_ema = EMA("AAPL", data["ohlcv"], length=26)  # longer EMA (e.g., 26 days)

        # Ensure both EMAs have been calculated and have values
        if short_ema is not None and long_ema is not None:
            # Check if the most recent short EMA crossed above the most recent long EMA
            if short_ema[-1] > long_ema[-1] and short_ema[-2] <= long_ema[-2]:
                log(f"Short EMA crossed above Long EMA for AAPL, buying signal")
                aapl_stake = 1  # Set full allocation to AAPL
            else:
                log(f"No EMA crossover signal for AAPL")
        
        # Return the target allocation with the calculated AAPL stake
        return TargetAllocation({"AAPL": aapl_stake})
import pytest
from at_common_workflow import Context
from at_common_tasks import init_storage
from at_common_tasks.tasks.data.stock import stock_get_quotation, stock_get_overview, stock_get_candlesticks, stock_get_indicators, stock_get_annual_income_statements, stock_get_quarterly_income_statements, stock_get_annual_balance_sheets, stock_get_quarterly_balance_sheets, stock_get_annual_cashflows, stock_get_quarterly_cashflows

from decimal import Decimal
from datetime import datetime


init_storage(
    host="192.168.50.234",
    port=3306,
    user="at_writer",
    password="at_writer@2024",
    database="at"
)

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_quotation_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_quotation(context)
    
    # Assert
    stock_quotation = context["stock_quotation"]
    assert stock_quotation["price"] > 0
    assert isinstance(stock_quotation["price"], float)
    assert "volume" in stock_quotation
    assert "previous_close" in stock_quotation
    assert "change" in stock_quotation
    assert "change_percentage" in stock_quotation

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_quotation_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act & Assert
    with pytest.raises(ValueError, match="No quotation found for symbol: INVALID"):
        await stock_get_quotation(context) 

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_overview_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_overview(context)
    
    # Assert
    stock_overview = context["stock_overview"]
    assert "exchange" in stock_overview
    assert "name" in stock_overview
    assert "description" in stock_overview
    assert "currency" in stock_overview
    assert "country" in stock_overview
    assert "address" in stock_overview
    assert "sector" in stock_overview
    assert "industry" in stock_overview
    assert "ceo" in stock_overview
    assert "ipo_date" in stock_overview

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_overview_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act & Assert
    with pytest.raises(ValueError, match="No overview found for symbol: INVALID"):
        await stock_get_overview(context)

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_candlesticks_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_candlesticks(context)
    
    # Assert
    candlesticks = context["stock_candlesticks"]
    assert isinstance(candlesticks, list)
    assert len(candlesticks) <= 30  # Verify limit is respected
    
    if len(candlesticks) > 0:
        first_candlestick = candlesticks[0]
        assert "time" in first_candlestick
        assert "open" in first_candlestick
        assert "high" in first_candlestick
        assert "low" in first_candlestick
        assert "close" in first_candlestick
        assert "volume" in first_candlestick
        print(first_candlestick["open"])
        # Verify data types and value ranges
        assert isinstance(first_candlestick["open"], (float, Decimal))
        assert isinstance(first_candlestick["volume"], (int, float))
        assert first_candlestick["high"] >= first_candlestick["low"]
        
        # Verify chronological order (newest first)
        if len(candlesticks) > 1:
            assert candlesticks[0]["time"] > candlesticks[1]["time"]

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_candlesticks_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act
    await stock_get_candlesticks(context)
    
    # Assert
    assert context["stock_candlesticks"] == []

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_indicators_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_indicators(context)
    
    # Assert
    indicators = context["stock_indicators"]
    assert isinstance(indicators, list)
    assert len(indicators) <= 30  # Verify limit is respected
    
    if len(indicators) > 0:
        first_indicator = indicators[0]
        # Verify presence of all indicator groups
        # Moving Averages
        assert all(key in first_indicator for key in ["sma5", "sma10", "sma20", "ema5", "ema10", "ema20"])
        # Momentum Indicators
        assert all(key in first_indicator for key in ["rsi", "macd", "macd_signal", "macd_hist"])
        # Stochastic
        assert all(key in first_indicator for key in ["slowk", "slowd"])
        # Bollinger Bands
        assert all(key in first_indicator for key in ["upper_band", "middle_band", "lower_band"])
        # Volume and Other Indicators
        assert all(key in first_indicator for key in ["obv", "roc", "willr", "atr"])
        # Trading Signals
        assert all(key in first_indicator for key in [
            "sig_ma_cross_5_10", "sig_ma_cross_10_20",
            "sig_rsi_overbought", "sig_rsi_oversold",
            "sig_macd_crossover", "sig_stoch_crossover",
            "sig_bb_breakout_up", "sig_bb_breakout_down",
            "sig_volume_spike", "sig_higher_high", "sig_lower_low"
        ])
        
        # Verify data types and value ranges
        assert isinstance(first_indicator["time"], (str, datetime))
        assert isinstance(first_indicator["rsi"], (float, Decimal))
        
        # Verify chronological order (newest first)
        if len(indicators) > 1:
            assert indicators[0]["time"] > indicators[1]["time"]

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_indicators_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act
    await stock_get_indicators(context)
    
    # Assert
    assert context["stock_indicators"] == []

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_annual_income_statements_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_annual_income_statements(context)
    
    # Assert
    statements = context["stock_annual_income_statements"]
    assert isinstance(statements, list)
    assert len(statements) <= 10  # Verify limit is respected
    
    if len(statements) > 0:
        first_statement = statements[0]
        # Verify essential income statement fields
        assert all(key in first_statement for key in [
            "fiscal_date_ending",
            "revenue",
            "gross_profit",
            "operating_income",
            "net_income",
            "eps",
            "ebitda"
        ])
        
        # Verify data types and basic validation
        assert isinstance(first_statement["revenue"], (int, float, Decimal))
        assert isinstance(first_statement["fiscal_date_ending"], (str, datetime))
        assert first_statement["revenue"] >= first_statement["gross_profit"]
        
        # Verify chronological order (newest first)
        if len(statements) > 1:
            assert statements[0]["fiscal_date_ending"] > statements[1]["fiscal_date_ending"]

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_quarterly_income_statements_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_quarterly_income_statements(context)
    
    # Assert
    statements = context["stock_quarterly_income_statements"]
    assert isinstance(statements, list)
    assert len(statements) <= 12  # Verify limit is respected
    
    if len(statements) > 0:
        first_statement = statements[0]
        # Verify essential income statement fields
        assert all(key in first_statement for key in [
            "fiscal_date_ending",
            "revenue",
            "gross_profit",
            "operating_income",
            "net_income",
            "eps",
            "ebitda"
        ])

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_annual_balance_sheets_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_annual_balance_sheets(context)
    
    # Assert
    statements = context["stock_annual_balance_sheets"]
    assert isinstance(statements, list)
    assert len(statements) <= 10
    
    if len(statements) > 0:
        first_statement = statements[0]
        # Verify essential balance sheet fields
        assert all(key in first_statement for key in [
            "fiscal_date_ending",
            "total_assets",
            "total_current_assets",
            "total_liabilities",
            "total_current_liabilities",
            "total_stockholders_equity"
        ])
        
        # Verify basic accounting equation
        assert abs(first_statement["total_assets"] - 
                  (first_statement["total_liabilities"] + 
                   first_statement["total_stockholders_equity"])) < 1  # Allow for rounding

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_quarterly_balance_sheets_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_quarterly_balance_sheets(context)
    
    # Assert
    statements = context["stock_quarterly_balance_sheets"]
    assert isinstance(statements, list)
    assert len(statements) <= 12
    
    if len(statements) > 0:
        first_statement = statements[0]
        assert all(key in first_statement for key in [
            "fiscal_date_ending",
            "total_assets",
            "total_current_assets",
            "total_liabilities",
            "total_current_liabilities",
            "total_stockholders_equity"
        ])

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_annual_cashflows_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_annual_cashflows(context)
    
    # Assert
    statements = context["stock_annual_cashflows"]
    assert isinstance(statements, list)
    assert len(statements) <= 10
    
    if len(statements) > 0:
        first_statement = statements[0]
        # Verify essential cash flow fields
        assert all(key in first_statement for key in [
            "fiscal_date_ending",
            "operating_cash_flow",
            "capital_expenditure",
            "dividends_paid",
            "free_cash_flow"
        ])
        
        # Verify free cash flow calculation
        assert abs(first_statement["free_cash_flow"] - 
                  (first_statement["operating_cash_flow"] - 
                   first_statement["capital_expenditure"])) < 1  # Allow for rounding

@pytest.mark.asyncio(loop_scope="session")
async def test_stock_get_quarterly_cashflows_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_quarterly_cashflows(context)
    
    # Assert
    statements = context["stock_quarterly_cashflows"]
    assert isinstance(statements, list)
    assert len(statements) <= 12
    
    if len(statements) > 0:
        first_statement = statements[0]
        assert all(key in first_statement for key in [
            "fiscal_date_ending",
            "operating_cash_flow",
            "capital_expenditure",
            "dividends_paid",
            "free_cash_flow"
        ])

# Add not found tests for each statement type
@pytest.mark.asyncio(loop_scope="session")
async def test_financial_statements_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act & Assert - test all statement types
    await stock_get_annual_income_statements(context)
    assert context["stock_annual_income_statements"] == []
    
    await stock_get_quarterly_income_statements(context)
    assert context["stock_quarterly_income_statements"] == []
    
    await stock_get_annual_balance_sheets(context)
    assert context["stock_annual_balance_sheets"] == []
    
    await stock_get_quarterly_balance_sheets(context)
    assert context["stock_quarterly_balance_sheets"] == []
    
    await stock_get_annual_cashflows(context)
    assert context["stock_annual_cashflows"] == []
    
    await stock_get_quarterly_cashflows(context)
    assert context["stock_quarterly_cashflows"] == []
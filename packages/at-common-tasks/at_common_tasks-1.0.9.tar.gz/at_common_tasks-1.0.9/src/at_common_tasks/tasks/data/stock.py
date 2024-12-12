from at_common_workflow import task, Context
from at_common_tasks.utils.storage import get_storage
from at_common_models.stock.quotation import QuotationModel
from at_common_models.stock.overview import OverviewModel
from at_common_models.stock.daily_candlestick import DailyCandlestickModel
from at_common_models.stock.daily_indicator import DailyIndicatorModel
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from at_common_models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from at_common_models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from at_common_tasks.utils.mappers import map_income_statement, map_balance_sheet_statement, map_cashflow_statement

@task(
    name="stock_get_overview",
    description="",
    requires={"symbol": str},
    provides={"stock_overview": dict}
)
async def stock_get_overview(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    overviews = await storage.query(
        model_class=OverviewModel,
        filters=[OverviewModel.symbol == symbol]
    )

    if len(overviews) == 0:
        raise ValueError(f"No overview found for symbol: {symbol}")

    if len(overviews) > 1:
        raise ValueError(f"Multiple overviews found for symbol: {symbol}, got {len(overviews)}")
    
    overview = overviews[0]

    context["stock_overview"] = {
        "exchange": overview.exchange,
        "name": overview.name,
        "description": overview.description,
        "currency": overview.currency,
        "country": overview.country,
        "address": overview.address,
        "sector": overview.sector,
        "industry": overview.industry,
        "ceo": overview.ceo,
        "ipo_date": overview.ipo_date
    }

@task(
    name="stock_get_quotation",
    description="Retrieves the latest stock price for a given symbol",
    requires={"symbol": str},
    provides={"stock_quotation": dict}
)
async def stock_get_quotation(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    quotations = await storage.query(
        model_class=QuotationModel,
        filters=[QuotationModel.symbol == symbol]
    )

    if len(quotations) == 0:
        raise ValueError(f"No quotation found for symbol: {symbol}")
    
    if len(quotations) > 1:
        raise ValueError(f"Multiple quotations found for symbol: {symbol}, got {len(quotations)}")
    
    quotation = quotations[0]
    context["stock_quotation"] = {
        "price": quotation.price,
        "volume": quotation.volume,
        "previous_close": quotation.previous_close,
        "change": quotation.change,
        "change_percentage": quotation.change_percentage
    }

@task(
    name="stock_get_candlesticks",
    description="Retrieves daily candlestick data for a given symbol",
    requires={"symbol": str},
    provides={"stock_candlesticks": list}
)
async def stock_get_candlesticks(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    candlesticks = await storage.query(
        model_class=DailyCandlestickModel,
        filters=[DailyCandlestickModel.symbol == symbol],
        sort=[DailyCandlestickModel.time.desc()],
        limit=30
    )

    context["stock_candlesticks"] = [{
        "time": candlestick.time,
        "open": candlestick.open,
        "high": candlestick.high,
        "low": candlestick.low,
        "close": candlestick.close,
        "volume": candlestick.volume
    } for candlestick in candlesticks]

@task(
    name="stock_get_indicators",
    description="Retrieves daily technical indicators for a given symbol",
    requires={"symbol": str},
    provides={"stock_indicators": list}
)
async def stock_get_indicators(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    indicators = await storage.query(
        model_class=DailyIndicatorModel,
        filters=[DailyIndicatorModel.symbol == symbol],
        sort=[DailyIndicatorModel.time.desc()],
        limit=30
    )

    context["stock_indicators"] = [{
        "time": indicator.time,
        # Moving Averages
        "sma5": indicator.sma5,
        "sma10": indicator.sma10,
        "sma20": indicator.sma20,
        "ema5": indicator.ema5,
        "ema10": indicator.ema10,
        "ema20": indicator.ema20,
        # Momentum Indicators
        "rsi": indicator.rsi,
        "macd": indicator.macd,
        "macd_signal": indicator.macd_signal,
        "macd_hist": indicator.macd_hist,
        # Stochastic
        "slowk": indicator.slowk,
        "slowd": indicator.slowd,
        # Bollinger Bands
        "upper_band": indicator.upper_band,
        "middle_band": indicator.middle_band,
        "lower_band": indicator.lower_band,
        # Volume and Other Indicators
        "obv": indicator.obv,
        "roc": indicator.roc,
        "willr": indicator.willr,
        "atr": indicator.atr,
        # Trading Signals
        "sig_ma_cross_5_10": indicator.sig_ma_cross_5_10,
        "sig_ma_cross_10_20": indicator.sig_ma_cross_10_20,
        "sig_rsi_overbought": indicator.sig_rsi_overbought,
        "sig_rsi_oversold": indicator.sig_rsi_oversold,
        "sig_macd_crossover": indicator.sig_macd_crossover,
        "sig_stoch_crossover": indicator.sig_stoch_crossover,
        "sig_bb_breakout_up": indicator.sig_bb_breakout_up,
        "sig_bb_breakout_down": indicator.sig_bb_breakout_down,
        "sig_volume_spike": indicator.sig_volume_spike,
        "sig_higher_high": indicator.sig_higher_high,
        "sig_lower_low": indicator.sig_lower_low
    } for indicator in indicators]

@task(
    name="stock_get_annual_income_statements",
    description="Retrieves annual income statements for a given symbol",
    requires={"symbol": str},
    provides={"stock_annual_income_statements": list}
)
async def stock_get_annual_income_statements(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    statements = await storage.query(
        model_class=AnnualIncomeStatementModel,
        filters=[AnnualIncomeStatementModel.symbol == symbol],
        sort=[AnnualIncomeStatementModel.fiscal_date_ending.desc()],
        limit=10
    )
    context["stock_annual_income_statements"] = [map_income_statement(statement) for statement in statements]

@task(
    name="stock_get_quarterly_income_statements",
    description="Retrieves quarterly income statements for a given symbol",
    requires={"symbol": str},
    provides={"stock_quarterly_income_statements": list}
)
async def stock_get_quarterly_income_statements(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    statements = await storage.query(
        model_class=QuarterlyIncomeStatementModel,
        filters=[QuarterlyIncomeStatementModel.symbol == symbol],
        sort=[QuarterlyIncomeStatementModel.fiscal_date_ending.desc()],
        limit=12
    )
    context["stock_quarterly_income_statements"] = [map_income_statement(statement) for statement in statements]

@task(
    name="stock_get_annual_balance_sheets",
    description="Retrieves annual balance sheets for a given symbol",
    requires={"symbol": str},
    provides={"stock_annual_balance_sheets": list}
)
async def stock_get_annual_balance_sheets(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    statements = await storage.query(
        model_class=AnnualBalanceSheetStatementModel,
        filters=[AnnualBalanceSheetStatementModel.symbol == symbol],
        sort=[AnnualBalanceSheetStatementModel.fiscal_date_ending.desc()],
        limit=10
    )
    context["stock_annual_balance_sheets"] = [map_balance_sheet_statement(statement) for statement in statements]

@task(
    name="stock_get_quarterly_balance_sheets",
    description="Retrieves quarterly balance sheets for a given symbol",
    requires={"symbol": str},
    provides={"stock_quarterly_balance_sheets": list}
)
async def stock_get_quarterly_balance_sheets(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    statements = await storage.query(
        model_class=QuarterBalanceSheetStatementModel,
        filters=[QuarterBalanceSheetStatementModel.symbol == symbol],
        sort=[QuarterBalanceSheetStatementModel.fiscal_date_ending.desc()],
        limit=12
    )
    context["stock_quarterly_balance_sheets"] = [map_balance_sheet_statement(statement) for statement in statements]

@task(
    name="stock_get_annual_cashflows",
    description="Retrieves annual cashflow statements for a given symbol",
    requires={"symbol": str},
    provides={"stock_annual_cashflows": list}
)
async def stock_get_annual_cashflows(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    statements = await storage.query(
        model_class=AnnualCashFlowStatementModel,
        filters=[AnnualCashFlowStatementModel.symbol == symbol],
        sort=[AnnualCashFlowStatementModel.fiscal_date_ending.desc()],
        limit=10
    )
    context["stock_annual_cashflows"] = [map_cashflow_statement(statement) for statement in statements]

@task(
    name="stock_get_quarterly_cashflows",
    description="Retrieves quarterly cashflow statements for a given symbol",
    requires={"symbol": str},
    provides={"stock_quarterly_cashflows": list}
)
async def stock_get_quarterly_cashflows(context: 'Context'):
    symbol = context["symbol"]
    storage = get_storage()
    statements = await storage.query(
        model_class=QuarterCashflowStatementModel,
        filters=[QuarterCashflowStatementModel.symbol == symbol],
        sort=[QuarterCashflowStatementModel.fiscal_date_ending.desc()],
        limit=12
    )
    context["stock_quarterly_cashflows"] = [map_cashflow_statement(statement) for statement in statements]
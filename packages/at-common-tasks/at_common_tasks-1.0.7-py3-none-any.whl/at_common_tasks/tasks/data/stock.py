from at_common_workflow import task, Context
from at_common_tasks.utils.storage import get_storage
from at_common_models.stock.quotation import QuotationModel as StockQuotationModel
from at_common_models.stock.overview import OverviewModel as StockOverviewModel

@task(
    name="stock_get_overview",
    description="",
    requires={"symbol": str},
    provides={"stock_overview": dict}
)
async def stock_get_overview(context: 'Context'):
    symbol = context["symbol"]
    overviews = get_storage().query(
        model_class=StockOverviewModel,
        filters=[StockOverviewModel.symbol == symbol]
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
    provides={"stock_price": dict}
)
async def stock_get_quotation(context: 'Context'):
    symbol = context["symbol"]
    quotations = get_storage().query(
        model_class=StockQuotationModel,
        filters=[StockQuotationModel.symbol == symbol]
    )

    if len(quotations) == 0:
        raise ValueError(f"No quotation found for symbol: {symbol}")
    
    if len(quotations) > 1:
        raise ValueError(f"Multiple quotations found for symbol: {symbol}, got {len(quotations)}")
    
    quotation = quotations[0]
    context["stock_price"] = {
        "price": quotation.price,
        "volume": quotation.volume,
        "previous_close": quotation.previous_close,
        "change": quotation.change,
        "change_percentage": quotation.change_percentage
    }
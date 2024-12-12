import pytest
from at_common_workflow import Context
from at_common_tasks import init_storage
from at_common_tasks.tasks.data.stock import stock_get_quotation, stock_get_overview


init_storage(
    host="192.168.50.234",
    port=3306,
    user="at_writer",
    password="at_writer@2024",
    database="at"
)

@pytest.mark.asyncio
async def test_stock_get_quotation_success():
    # Arrange
    context = Context()
    context["symbol"] = "AAPL"
    
    # Act
    await stock_get_quotation(context)
    
    # Assert
    stock_price = context["stock_price"]
    assert stock_price["price"] > 0
    assert isinstance(stock_price["price"], float)
    assert "volume" in stock_price
    assert "previous_close" in stock_price
    assert "change" in stock_price
    assert "change_percentage" in stock_price

@pytest.mark.asyncio
async def test_stock_get_quotation_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act & Assert
    with pytest.raises(ValueError, match="No quotation found for symbol: INVALID"):
        await stock_get_quotation(context) 

@pytest.mark.asyncio
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

@pytest.mark.asyncio
async def test_stock_get_overview_not_found():
    # Arrange
    context = Context()
    context["symbol"] = "INVALID"
    
    # Act & Assert
    with pytest.raises(ValueError, match="No overview found for symbol: INVALID"):
        await stock_get_overview(context)
import pytest
from at_common_workflow import Context
from at_common_tasks.tasks.example import echo, reverse, add_integers

@pytest.mark.asyncio
async def test_echo():
    context = Context()
    context["in_msg"] = "Hello"
    await echo(context)
    assert context["out_msg"] == "Hello"

@pytest.mark.asyncio
async def test_reverse():
    context = Context()
    context["in_msg"] = "Hello"
    await reverse(context)
    assert context["out_msg"] == "olleH"

@pytest.mark.asyncio
async def test_add_integers():
    context = Context()
    context["num1"] = 5
    context["num2"] = 3
    await add_integers(context)
    assert context["result"] == 8
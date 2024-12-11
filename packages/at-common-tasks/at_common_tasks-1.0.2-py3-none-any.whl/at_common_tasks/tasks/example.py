from at_common_workflow import task, Context

@task(
    name="echo",
    description="",
    requires={"in_msg":str},
    provides={"out_msg":str}
)
async def echo(context: 'Context'):
    context["out_msg"] = context["in_msg"]

@task(
    name="reverse",
    description="",
    requires={"in_msg":str},
    provides={"out_msg":str}
)
async def reverse(context: 'Context'):
    context["out_msg"] = context["in_msg"][::-1]

@task(
    name="add_integers",
    description="Adds two integers and stores the result in the context",
    requires={"num1":int, "num2":int},
    provides={"result":int}
)
async def add_integers(context: 'Context'):
    context["result"] = context["num1"] + context["num2"]
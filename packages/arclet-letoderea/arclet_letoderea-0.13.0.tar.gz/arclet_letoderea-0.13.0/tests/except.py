import asyncio

from arclet.letoderea import BaseEvent, Contexts, bind, es, provide, subscribe


class TestEvent(BaseEvent):
    async def gather(self, context: Contexts):
        context["name"] = "Letoderea"


@subscribe(TestEvent)
@bind(provide(int, "age", "a", _id="foo"))
@bind(provide(int, "age", "b", _id="bar"))
@bind(provide(int, "age", "c", _id="baz"))
async def test_subscriber(name: str, age: int):
    print(name, age)


async def main():
    await es.publish(TestEvent())


asyncio.run(main())

import asyncio

from easy_scrape.core.runner import Runner
from easy_scrape.crawlers.example_crawler import ExampleCrawler
from easy_scrape.middlewares.user_agent import UserAgentMiddleware
from easy_scrape.pipelines.print_pipeline import PrintPipeline


async def main():
    runner = Runner(concurrency=5, middlewares=[UserAgentMiddleware()], pipelines=[PrintPipeline()])
    await runner.run(ExampleCrawler())


if __name__ == "__main__":
    asyncio.run(main())


import argparse
import asyncio
import importlib
from typing import List, Optional

from easy_scrape.core.runner import Runner
from easy_scrape.core.middleware import BaseMiddleware
from easy_scrape.core.pipeline import BasePipeline
from easy_scrape.middlewares.user_agent import UserAgentMiddleware
from easy_scrape.pipelines.print_pipeline import PrintPipeline


def load_crawler(dotted: str):
    if ":" not in dotted:
        raise ValueError("Crawler path must be 'module:ClassName'")
    module_name, class_name = dotted.split(":", 1)
    mod = importlib.import_module(module_name)
    cls = getattr(mod, class_name)
    return cls


def run_cmd(args: argparse.Namespace):
    crawler_cls = load_crawler(args.crawler)
    crawler = crawler_cls()
    if args.start_url:
        crawler.start_urls = list(args.start_url)

    middlewares: List[BaseMiddleware] = [UserAgentMiddleware()]
    pipelines: List[BasePipeline] = [PrintPipeline()]

    runner = Runner(concurrency=args.concurrency, middlewares=middlewares, pipelines=pipelines)
    asyncio.run(runner.run(crawler))


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(prog="easy-scrape", description="Run easy-scrape crawlers")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run a crawler")
    run_p.add_argument("crawler", help="Dotted path 'module:ClassName' to crawler")
    run_p.add_argument("-c", "--concurrency", type=int, default=10, help="Concurrent requests")
    run_p.add_argument("-u", "--start-url", action="append", help="Override start URL (can repeat)")
    run_p.set_defaults(func=run_cmd)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()


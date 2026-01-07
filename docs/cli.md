CLI Usage

Run a crawler

- `python -m easy_scrape.cli run <module:Class>`
  - Example: `python -m easy_scrape.cli run easy_scrape.crawlers.example_crawler:ExampleCrawler`

Flags

- `-c, --concurrency <int>`: concurrent requests (default 10)
- `-u, --start-url <url>`: override/add start URL (repeatable)

Examples

- High concurrency: `... -c 50`
- Multiple seeds: `... -u https://a -u https://b`

Help

- `python -m easy_scrape.cli -h`

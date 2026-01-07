Troubleshooting

Common Issues

- Import errors: Ensure your crawler is under `easy_scrape/crawlers/` and the dotted path is correct: `module:Class`.
- SSL or blocked requests: Try adding headers via middleware; test against `https://example.org/` first.
- Playwright not installed: `pip install playwright` and `python -m playwright install chromium`.
- Network blocks or CAPTCHAs: Respect robots, add delays, use proxies where permitted.

Debugging Tips

- Print inside `parse()` to verify selectors and outputs.
- Add a logging middleware to log requests/responses (status codes, URLs).
- Lower concurrency to isolate issues: `-c 1`.

Getting Help

- File an issue using the templates. Include steps, expected vs actual, and environment details.

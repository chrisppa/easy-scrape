Contributing to easy-scrape

Thanks for your interest in contributing! This project aims to make scraping easy with a small, async-first framework.

Getting Started

- Fork and clone the repo.
- Create a virtual environment and install deps:
  - Unix/macOS: `python3 -m venv .venv && source .venv/bin/activate`
  - Windows (PowerShell): `py -m venv .venv; .venv\\Scripts\\Activate.ps1`
  - Install: `pip install -r requirements.txt`

Development Workflow

- Run a quick smoke check: `python -m compileall easy_scrape examples` and `python -m easy_scrape.cli -h`
- Try the example crawler locally: `python -m easy_scrape.cli run easy_scrape.crawlers.example_crawler:ExampleCrawler`
- Keep changes focused and small. Update docs when behavior changes.
- Follow Conventional Commits for messages (e.g., `feat:`, `fix:`, `docs:`).

Code Style

- Keep it simple. Prefer readability over cleverness.
- Async by default for I/O. Avoid thread-based concurrency.
- Avoid adding heavy dependencies without discussion.

Reporting Issues

- Search existing issues first.
- Provide clear steps to reproduce, expected vs. actual behavior, and environment details.

Security

- Please do not open public issues for security vulnerabilities.
- Report privately via GitHub Security Advisories: https://github.com/chrisppa/easy-scrape/security/advisories/new

Code of Conduct

- By participating, you agree to abide by our Code of Conduct (CODE_OF_CONDUCT.md).


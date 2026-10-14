# Job Search Agent — Architecture

## First goal

Collect jobs from permitted sources, normalize them, remove duplicates, and display them in one searchable UI.

```text
Job sources -> Collect -> Clean -> Deduplicate -> Store -> API -> Web UI
```

Do not build AI matching or automatic applications first. Make job collection reliable before adding intelligence.

## Read in this order

1. [High-level architecture](1.high-level-architecture.md)
2. [Low-level architecture](2.low-level-architecture.md)
3. [Technology choices](3.technologies.md)
4. [Database and API design](4.database-and-api.md)
5. [Scraping strategy](5.scraping-strategy.md)
6. [MVP implementation plan](6.mvp-plan.md)

## Recommended first sources

Start with public ATS job feeds such as Greenhouse and Lever. Add direct HTML scraping only where the site's terms and `robots.txt` permit it.

Do **not** scrape LinkedIn directly. LinkedIn explicitly prohibits crawlers and scraping software. You may store a LinkedIn job URL that a user manually provides, or use an officially approved integration.

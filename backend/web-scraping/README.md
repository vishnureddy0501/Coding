# Job Portal Aggregator: Architecture Guide

Goal: collect jobs from allowed sources, clean and combine them, then show them in one portal.

This is an architecture-first guide. No scraper code yet.

## Read in this order

1. [Plan](plan.md)
2. [Big picture architecture](01-big-picture-architecture.md)
3. [Sources and connectors](02-sources-and-connectors.md)
4. [Ingestion pipeline](03-ingestion-pipeline.md)
5. [Database design](04-database-design.md)
6. [Search API and frontend](05-search-api-and-frontend.md)
7. [Reliability and scaling](06-reliability-and-scaling.md)
8. [Local, dev, and production](07-environments-and-deployment.md)
9. [Build order](08-build-order.md)

## One sentence summary

Each source has a small connector. Connectors send raw jobs to a queue; workers clean, deduplicate, and save them; the user-facing API reads only clean saved jobs.

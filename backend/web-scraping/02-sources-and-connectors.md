# 2. Sources and Connectors

## Use sources in this order

1. Official APIs, partner feeds, or employer career pages.
2. Public pages only when their terms and robots rules allow automated access.
3. Never design around bypassing login, CAPTCHAs, rate limits, or other access controls.

Every portal has its own rules and page structure. Check its current terms before enabling that source.

## One connector per source

```text
connectors/
├── base_connector
├── company_careers_connector
├── source_a_connector
└── source_b_connector
```

Every connector produces the same normalized output even if the source returns different fields.

```text
Source A: jobTitle, employerName, applyLink
Source B: title, company, url
                         │
                         ▼
Your shape: title, company_name, apply_url
```

## Common normalized job fields

```text
title
company_name
location_text
workplace_type          # remote / hybrid / onsite / unknown
employment_type         # full-time / internship / contract
description
skills                  # extracted later if needed
apply_url
source_name
source_job_id
posted_at
collected_at
```

## Source configuration belongs in the database

Example settings stored for a source:

```text
source: "Company careers"
enabled: true
fetch_frequency_minutes: 60
last_success_at: ...
rate_limit_per_minute: 10
```

You can disable one broken source without deploying new code.

## Portal changes are normal

```text
Source A changes → only Source A connector fails
                 → other sources still work
                 → alert identifies the connector to update
```

Never mix source-specific parsing logic into the user-facing job API.

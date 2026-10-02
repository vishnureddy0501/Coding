# Frontend Performance — Practical Learning Guide

This folder focuses on how to **find and fix real performance problems**.

## Learn in this order

1. [Measure with Chrome DevTools](./1.chrome-devtools.md)
2. [Improve page loading and network requests](./2.loading-and-network.md)
3. [Fix slow JavaScript and rendering](./3.javascript-and-rendering.md)
4. [Optimize images, CSS, and fonts](./4.images-css-fonts.md)
5. [Improve Vue application performance](./5.vue-performance.md)
6. [Caching, APIs, and production monitoring](./6.caching-and-monitoring.md)
7. [Practical checklist and interview answers](./7.checklist-and-interview.md)

## The main rule

Do not optimize based on guessing.

```text
Measure
  ↓
Find the slow part
  ↓
Make one change
  ↓
Measure again
```

## What good performance means

A page should:

- Show its main content quickly.
- Respond quickly when the user clicks or types.
- Avoid unexpected layout movement.
- Download only the resources needed now.
- Avoid unnecessary JavaScript and rendering.

The three Core Web Vitals are:

| Metric | What it tells you | Good target |
|---|---|---:|
| **LCP** | How quickly the main visible content appears | 2.5 seconds or less |
| **INP** | How quickly the page responds to interactions | 200 ms or less |
| **CLS** | How much the layout unexpectedly moves | 0.1 or less |

Use these as signals. The DevTools investigation tells you what is causing the bad score.


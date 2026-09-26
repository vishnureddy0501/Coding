# Express API Testing — Interview Guide

This folder contains the main concepts and examples needed for an Express API testing interview.

## Suggested Order

1. [Start Here: Concepts and Terms](./0.start-here.md)
2. [Jest Basics](./0.1-jest-basics.md)
3. [Supertest Basics](./0.2-supertest-basics.md)
4. [Mocks](./0.3.mocks.md)
5. [API Testing Fundamentals](./1.api-testing-fundamentals.md)
6. [Writing Express API Tests](./2.writing-express-api-tests.md)
7. [Interview Revision](./3.interview-revision.md)

## Tools Used in the Examples

- **Jest:** runs tests and provides assertions, setup hooks, and mocks.
- **Supertest:** sends HTTP-style requests directly to an Express application.

```bash
npm install --save-dev jest supertest
```

The examples use ES modules with `import` and `export`. The project should set `"type": "module"` in `package.json`.

## What You Should Be Able to Do

After studying these notes, you should be able to:

- Explain unit, integration, and end-to-end API tests.
- Write a Supertest test for an Express endpoint.
- Test success, validation, authentication, and not-found cases.
- Prepare and clean test data correctly.
- Decide when to use a real dependency and when to mock one.
- Explain what makes an API test reliable.

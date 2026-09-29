# MCP Servers — Interview Guide

This folder covers the Model Context Protocol concepts most useful in software-engineering and AI-agent interviews.

## Learning Order

1. [MCP Fundamentals](./1.fundamentals.md)
2. [Architecture and Request Flow](./2.architecture-and-flow.md)
3. [Designing an MCP Server](./3.designing-a-server.md)
4. [Security and Production Concerns](./4.security-and-production.md)
5. [Interview Questions](./5.interview-questions.md)

## One-Line Definition

> MCP is an open protocol that standardizes how AI applications discover and use external tools, data, and reusable prompts.

## What to Remember

```text
MCP host → MCP client → MCP server → external system
```

- The host is the AI application.
- The client manages a connection to a server.
- The server exposes capabilities.
- Tools perform operations.
- Resources provide readable context.
- Prompts provide reusable templates.
- `stdio` is common for local servers.
- Streamable HTTP is used for remote servers.
- Authentication is not the same as authorization.
- Sensitive actions should require approval.

## References

- [OpenAI: MCP Server Concepts](https://developers.openai.com/plugins/concepts/mcp-server)
- [OpenAI: MCP Connections](https://developers.openai.com/api/docs/guides/agents-api/tools/mcp)
- [MCP TypeScript SDK](https://ts.sdk.modelcontextprotocol.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)


# MCP for the Action Items Library Chatbot

This course teaches MCP through one real requirement:

> Build a chatbot that answers questions about Aviso's Action Items Library using MongoDB.

We will not study unrelated MCP examples or connect many external systems.

## What the chatbot should answer

```text
"Find action-item templates related to kickoff"
"Show HIGH-priority templates"
"Give me details of this action_library_id"
"How many templates exist for each priority?"
```

The first version is **read-only**. It cannot create, update, or delete library entries.

## Learning order

1. [Understand the real requirement](1.requirement.md)
2. [Understand the architecture](2.architecture.md)
3. [Design the MCP tools](3.tools.md)
4. [Understand one complete question flow](4.question-flow.md)
5. [Build the custom server](5.build-the-server.md)
6. [Connect it to the chatbot](6.connect-chatbot.md)
7. [Security and production rules](7.security-and-production.md)
8. [How MCP should fit into the customer-success repository](8.production-code-arrangement.md)
9. [Interview internals and deployment](9.interview-internals-and-deployment.md)

Runnable learning server: [action-items-library-mcp](action-items-library-mcp/README.md)

## The only important idea

```text
The LLM understands the question.
The MCP server safely fetches the required MongoDB data.
The LLM turns that data into a useful answer.
```

The MCP server is not another database and does not train the LLM.

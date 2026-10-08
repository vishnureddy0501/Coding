# Chatbot scope contract

Replace every placeholder before implementation.

## 1. Product purpose

```text
The chatbot helps [USER ROLE] answer questions about [PROJECT DOMAIN]
using only [APPROVED SOURCES].
```

## 2. Initial user role

- Role:
- Authentication source:
- Tenant source:
- Record-access rule:

## 3. Data sources

| Source | Structured/document | Live/indexed | Approved | Freshness | Limit |
|---|---|---|---|---|---|
| Example Accounts API | structured | live | yes | request time | one account |

## 4. Entities and fields

### Entity: `[NAME]`

Allowed fields:

- 

Forbidden fields:

- 

Permission rule:

```text

```

## 5. Supported intents

### Intent 1: `[NAME]`

- Purpose:
- Required arguments:
- Optional arguments:
- Approved source:
- Allowed role:
- Maximum result size:
- Missing-data behavior:

Positive examples:

1. 
2. 
3. 
4. 
5. 

Negative/confusing examples:

1. 
2. 
3. 

### Intent 2: `[NAME]`

- Purpose:
- Required arguments:
- Optional arguments:
- Approved source:
- Allowed role:
- Maximum result size:
- Missing-data behavior:

Positive examples:

1. 
2. 
3. 
4. 
5. 

Negative/confusing examples:

1. 
2. 
3. 

### Intent 3: `[NAME]`

- Purpose:
- Required arguments:
- Optional arguments:
- Approved source:
- Allowed role:
- Maximum result size:
- Missing-data behavior:

Positive examples:

1. 
2. 
3. 
4. 
5. 

Negative/confusing examples:

1. 
2. 
3. 

## 6. Unsupported requests

Topics:

- general knowledge;
- 

Operations:

- write/update/delete operations;
- arbitrary database queries;
- 

## 7. Public responses

Answered:

```text
[The answer is generated from cited evidence.]
```

Needs clarification:

```text

```

No information:

```text
I could not find that information in the available project data.
```

Out of scope:

```text
I can only answer questions about this project's approved data.
```

Temporarily unavailable:

```text
I could not access the project data right now. Please try again.
```

## 8. Source and citation rules

- Tool results should identify:
- Documents should identify:
- Source details visible to users:
- Source details retained only in logs:

## 9. Open decisions

- 

# Gmail OAuth 2.0 — Quick Interview Notes

## One-line revision

```text
Popup → authorization code → backend → encrypted refresh token
      → short-lived access token → Gmail API
```

we have scope variable in the popup. we can define which permissions we want. send email/read email ....

## Why do we use it?

Gmail OAuth allows our application to send or read emails with the user's permission, without asking for their Google password.

---

## Simple flow

```text
User clicks Connect Gmail
        ↓
Google login and consent popup opens
        ↓
Google returns an authorization code
        ↓
Frontend sends the code to Express.js
        ↓
Backend exchanges the code for tokens
        ↓
Backend stores the refresh token securely
        ↓
Backend uses the access token to call Gmail APIs
```

Token endpoint:

```http
POST https://oauth2.googleapis.com/token
```

---

## Where do we store everything?

| Value | Storage |
|---|---|
| Application session | Secure HttpOnly cookie; session data in Redis/DB |
| Authorization code | Do not store; send it to the backend immediately |
| Access token | Backend memory or Redis; short-lived |
| Refresh token | Encrypted in the backend database |
| Google client secret | Backend secret manager/environment variable |

Never store Google access tokens, refresh tokens, or the client secret in Vuex, `localStorage`, or `sessionStorage`.

The frontend should store only:

```js
{
  gmailConnected: true,
  email: 'user@company.com'
}
```

---

## Access token versus refresh token

### Access token

- Used to call Gmail APIs.
- Short-lived.
- Sent as `Authorization: Bearer <token>`.

### Refresh token

- Used to obtain a new access token.
- Long-lived but can be revoked.
- Required for scheduled emails when the user is offline.
- Must be encrypted and stored only on the backend.

```text
Access token expired
        ↓
Backend uses refresh token
        ↓
Google returns a new access token
        ↓
Backend calls Gmail API
```

If the refresh token is rejected, mark Gmail as disconnected and ask the user to connect again.

---

## Can we connect Gmail without reloading the website?

**Yes.** Use Google Identity Services in popup mode:

---

## Backend responsibility

The Express backend:

1. Verifies the logged-in user and OAuth request.
2. Exchanges the authorization code for tokens.
3. Encrypts and stores the refresh token.
4. Uses or refreshes the access token.
5. Calls Gmail APIs.

Example Gmail API:

```http
POST /gmail/v1/users/me/messages/send
```

Do not return Google tokens to the frontend.

---

## Disconnect flow

```text
User clicks Disconnect
        ↓
Backend revokes Google access
        ↓
Delete stored tokens
        ↓
Stop future scheduled emails
```

---

## Interview answer

> We use Google's OAuth 2.0 authorization-code flow. The user clicks Connect Gmail, and Google consent opens in a popup, so the main website does not reload. Google returns a temporary authorization code, which the frontend sends to our Express backend.
>
> The backend exchanges the code for access and refresh tokens. We keep the short-lived access token in backend memory or Redis and store the refresh token encrypted in the database. The frontend stores only the connection status and never receives Google tokens.
>
> When the access token expires, the backend uses the refresh token to obtain another access token. If the refresh token is revoked, we ask the user to reconnect Gmail.


---

## How does the application know the access token expired?

When Google provides an access token, it also provides its lifetime:

```json
{
  "access_token": "access_token_value",
  "expires_in": 3600,
  "refresh_token": "refresh_token_value"
}
```

`expires_in: 3600` means the access token is valid for approximately one hour.

The backend calculates and stores the expiry time:

```js
const accessTokenExpiresAt = Date.now() + expiresIn * 1000;
```

Before calling Gmail, check the expiry with a small safety buffer:

```js
if (Date.now() >= accessTokenExpiresAt - 5 * 60 * 1000) {
  // Use the refresh token to get a new access token.
}

// Call Gmail using the valid access token.
```

Therefore, we do **not** need to call Gmail first just to discover that the token expired.

```text
Need to call Gmail
        ↓
Check accessTokenExpiresAt
        ↓
Token is still valid? ── Yes → Call Gmail
        ↓ No
Use refresh token to get a new access token
        ↓
Save the new token and expiry time
        ↓
Call Gmail
```

Google's Node.js client library can perform this check and refresh automatically when it has the refresh token and expiry information.

### What if Gmail still returns `401 Unauthorized`?

The stored expiry time is the normal check. However, a token could be revoked before its expected expiry.

In that case:

1. Try refreshing the access token.
2. Retry the Gmail request only once.
3. If refreshing fails, mark the integration as `reauthorization_required`.
4. Ask the user to connect Gmail again.

Do not retry continuously.

### Interview answer

> Google returns `expires_in` along with the access token. The backend uses it to calculate `accessTokenExpiresAt`. Before calling Gmail, we check that time with a small buffer. If the token is close to expiry, we use the refresh token to obtain a new access token first. A Gmail `401` followed by one refresh and retry is only a fallback for cases such as early token revocation.

# API Contracts: Auth Service

**Base URL**: `/api/v1/auth/`  
**Upstream**: `http://auth-service:8000`

---

## POST /api/v1/auth/register

Register a new customer account.

**Auth Required**: No

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Validation**:
- `name`: required, 1-150 chars
- `email`: required, valid email, unique
- `password`: required, min 8 chars, must contain uppercase + lowercase + digit

**Response 201**:
```json
{
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "customer"
  }
}
```

**Response 400**: Validation error (duplicate email, weak password)  
**Side Effect**: Publishes `user.registered` event → Email service sends welcome email

---

## POST /api/v1/auth/login

Authenticate user and issue JWT tokens.

**Auth Required**: No

**Request**:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response 200**:
```json
{
  "data": {
    "user": {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "customer"
    }
  }
}
```

Sets httpOnly cookies:
- `access_token`: JWT, 15 min expiry
- `refresh_token`: JWT, 7 day expiry

**Response 401**: Invalid credentials  
**Response 423**: Account locked (after 5 failed attempts)

---

## POST /api/v1/auth/refresh

Refresh the access token using refresh token cookie.

**Auth Required**: No (uses refresh_token cookie)

**Response 200**: New `access_token` cookie set  
**Response 401**: Invalid or expired refresh token

---

## POST /api/v1/auth/logout

Invalidate the current refresh token.

**Auth Required**: Yes

**Response 204**: Cookies cleared, refresh token blacklisted

---

## GET /api/v1/auth/me

Get current user profile.

**Auth Required**: Yes

**Response 200**:
```json
{
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "customer",
    "is_email_verified": true,
    "created_at": "2026-03-04T12:00:00Z"
  }
}
```

---

## POST /api/v1/auth/forgot-password

Request password reset email.

**Auth Required**: No

**Request**:
```json
{
  "email": "john@example.com"
}
```

**Response 200**: Always returns success (prevents email enumeration)  
**Side Effect**: If email exists, publishes `user.password_reset_requested` event

---

## POST /api/v1/auth/reset-password

Reset password with token from email link.

**Auth Required**: No

**Request**:
```json
{
  "token": "reset-token-from-email",
  "new_password": "NewSecurePass456"
}
```

**Response 200**: Password updated  
**Response 400**: Invalid/expired token or weak password

# authController.js

## Description
The `authController.js` file contains the implementation of various functions related to user authentication and management. These functions interact with the `authModel` module to perform operations such as user signup, signin, updating user data, deleting users, and more. The file also includes helper functions and dependencies such as `jsonwebtoken` for token generation and verification.

## Examples
Here are some examples of how to use the functions in this file:

1. Signing up a new user:
```javascript
const newUser = {
  name: "John Doe",
  email: "john@example.com",
  password: "password123",
  type: "user"
};

authController.signup(newUser, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

2. Signing in an existing user:
```javascript
const credentials = {
  email: "john@example.com",
  password: "password123"
};

authController.signin(credentials, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

## Methods

### signup(request, response, next)
Creates a new user in the database.

- `request` (Object): JSON object containing all the information from the `GET` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### signin(request, response, next)
Looks for a user information and if correct returns a JWT token and user data.

- `request` (Object): JSON object containing all the information from the `GET` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### getAllUsers(request, response, next)
Get all users in the database.

- `request` (Object): JSON object containing all the information from the `GET` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### updateUser(request, response, next)
Updates user's data in the database.

- `request` (Object): JSON object containing all the information from the `GET` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### deleteUser(request, response, next)
Deletes user from the database.

- `request` (Object): JSON object containing all the information from the `DELETE` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### verifyToken(request, response, next)
Sends user information once the token sent was validated.

- `request` (Object): JSON object containing all the information from the `GET` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### changePassword(request, response, next)
Changes user's password.

- `request` (Object): JSON object containing all the information from the `POST` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### requestPasswordChange(request, response, next)
Checks if user exists and sends a restore link.

- `request` (Object): JSON object containing all the information from the `POST` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### checkRestoreRequest(request, response, next)
Checks if a restore request exists.

- `request` (Object): JSON object containing all the information from the `POST` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### restorePassword(request, response, next)
Restores password with the new one provided by the restore password form.

- `request` (Object): JSON object containing all the information from the `POST` request.
- `response` (Object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

## Technical Concepts
- JSON Web Tokens (JWT): This file uses the `jsonwebtoken` library to generate and verify JWT tokens. JWT is a compact, URL-safe means of representing claims to be transferred between two parties. It is commonly used for authentication and authorization purposes in web applications.

## Dependencies
- `jsonwebtoken`: A library for generating and verifying JSON Web Tokens.

## Variables
- `jwt`: The `jsonwebtoken` library for generating and verifying JSON Web Tokens.
- `authModel`: The module responsible for interacting with the database for authentication-related operations.
- `sendRestorePasswordEmail`: A helper function for sending restore password emails.
- `secret`: The secret key used for signing and verifying JWT tokens.

## Template File
N/A
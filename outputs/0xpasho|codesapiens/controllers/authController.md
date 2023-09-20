# authController.js

The `authController.js` file contains the implementation of various functions related to user authentication and management. These functions are used to handle user sign up, sign in, user data retrieval, user data update, user deletion, password change, and password restoration. This file exports these functions to be used in other parts of the application.

## Examples

Here are some examples of how to use the functions in this file:

1. Example of signing up a new user:
```javascript
const request = {
  body: {
    name: "John Doe",
    email: "johndoe@example.com",
    password: "password123",
    type: "user"
  }
};

const response = {
  send: (data) => {
    console.log(data);
  },
  status: (code) => {
    return {
      send: (data) => {
        console.log(data);
      }
    };
  }
};

const next = (error) => {
  console.error(error);
};

signup(request, response, next);
```

2. Example of signing in a user:
```javascript
const request = {
  body: {
    email: "johndoe@example.com",
    password: "password123"
  }
};

const response = {
  send: (data) => {
    console.log(data);
  },
  status: (code) => {
    return {
      send: (data) => {
        console.log(data);
      }
    };
  }
};

const next = (error) => {
  console.error(error);
};

signin(request, response, next);
```

## Methods

### signup(request, response, next)
Creates a new user in the database.

- `request` (Object): JSON that contains all the information from the `POST` request.
  - `name` (String): The name of the user.
  - `email` (String): The email of the user.
  - `password` (String): The password of the user.
  - `type` (String): The type of the user.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### signin(request, response, next)
Looks for a user information and if correct returns a JWT token and user data.

- `request` (Object): JSON that contains all the information from the `POST` request.
  - `email` (String): The email of the user.
  - `password` (String): The password of the user.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### getAllUsers(request, response, next)
Get all users in the database.

- `request` (Object): JSON that contains all the information from the `GET` request.
  - `page` (Number): The page number.
  - `pageLength` (Number): The number of users per page.
  - `search` (String): The search query to filter users.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### updateUser(request, response, next)
Updates user's data in the database.

- `request` (Object): JSON that contains all the information from the `PUT` request.
  - `params` (Object): The parameters of the request.
    - `id` (String): The ID of the user to update.
  - `body` (Object): The body of the request.
    - `name` (String): The new name of the user.
    - `email` (String): The new email of the user.
    - `type` (String): The new type of the user.
    - `password` (String): The new password of the user (optional).
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### deleteUser(request, response, next)
Deletes a user from the database.

- `request` (Object): JSON that contains all the information from the `DELETE` request.
  - `params` (Object): The parameters of the request.
    - `id` (String): The ID of the user to delete.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### changePassword(request, response, next)
Changes the password of a user.

- `request` (Object): JSON that contains all the information from the `PUT` request.
  - `iduser` (String): The ID of the user.
  - `newPassword` (String): The new password for the user.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### requestPasswordChange(request, response, next)
Checks if a user exists and sends a restore link.

- `request` (Object): JSON that contains all the information from the `POST` request.
  - `email` (String): The email of the user to check.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### checkRestoreRequest(request, response, next)
Checks if a restore request exists.

- `request` (Object): JSON that contains all the information from the `POST` request.
  - `idrestorepassword` (String): The ID of the restore request to check.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

### restorePassword(request, response, next)
Restores the password of a user with the new one provided.

- `request` (Object): JSON that contains all the information from the `POST` request.
  - `idrestorepassword` (String): The ID of the restore request.
  - `iduser` (String): The ID of the user.
  - `newPassword` (String): The new password for the user.
- `response` (Object): Server response to the final user.
- `next` (Function): Express method that jumps into the next route function.

## Technical Concepts

### JWT (JSON Web Token)
JSON Web Token (JWT) is an open standard for securely transmitting information between parties as a JSON object. It is commonly used for authentication and authorization purposes. In this file, JWT is used to sign and verify tokens for user authentication.

### Express
Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications. In this file, Express is used for routing and handling HTTP requests.

## Variables

The `authController.js` file uses the following variables:

- `jwt`: A module that provides functions for signing and verifying JSON Web Tokens.
- `authModel`: A module that provides functions for interacting with the authentication model.
- `sendRestorePasswordEmail`: A helper function for sending restore password emails.
- `secret`: The secret key used for signing and verifying JSON Web Tokens.

## Template File

This file does not contain a template.
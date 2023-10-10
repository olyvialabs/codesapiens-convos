authRoutes.js

Description:
This file contains the routes for authentication in the application. It includes various endpoints for user authentication, such as signing up, signing in, changing password, restoring password, and managing user accounts. The routes are implemented using the Express.js framework and are handled by the authController module.

Code Example:
```javascript
'use strict';

const express = require('express');
const api = express.Router();
const authController = require('../controllers/authController');
// Helpers
const { verifyToken } = require('../helpers/verifyToken');

api.get('/all_users', verifyToken, authController.getAllUsers);
api.get('/verify_token', verifyToken, authController.verifyToken);

api.post('/signup', verifyToken, authController.signup);
api.post('/signin', authController.signin);
api.post('/change_password', verifyToken, authController.changePassword);
api.post('/request_restore_password', authController.requestPasswordChange);
api.post('/check_restore_request', authController.checkRestoreRequest);
api.post('/restore_password', authController.restorePassword);

api.put('/user/:id', verifyToken, authController.updateUser);
api.delete('/user/:id', verifyToken, authController.deleteUser);

module.exports = api;
```

Methods:
1. getAllUsers
   - Description: Retrieves all users from the database.
   - HTTP Method: GET
   - Endpoint: /all_users
   - Parameters: None
   - Returns: An array of user objects.

2. verifyToken
   - Description: Verifies the authenticity of the token provided in the request header.
   - HTTP Method: GET
   - Endpoint: /verify_token
   - Parameters: None
   - Returns: A boolean indicating whether the token is valid or not.

3. signup
   - Description: Creates a new user account.
   - HTTP Method: POST
   - Endpoint: /signup
   - Parameters:
     - username: The username of the user (string)
     - password: The password of the user (string)
   - Returns: The newly created user object.

4. signin
   - Description: Authenticates the user and generates a token for subsequent requests.
   - HTTP Method: POST
   - Endpoint: /signin
   - Parameters:
     - username: The username of the user (string)
     - password: The password of the user (string)
   - Returns: A token object containing the generated token.

5. changePassword
   - Description: Changes the password of the authenticated user.
   - HTTP Method: POST
   - Endpoint: /change_password
   - Parameters:
     - oldPassword: The current password of the user (string)
     - newPassword: The new password to be set (string)
   - Returns: A success message indicating that the password has been changed.

6. requestPasswordChange
   - Description: Sends a password change request to the user's email address.
   - HTTP Method: POST
   - Endpoint: /request_restore_password
   - Parameters:
     - email: The email address of the user (string)
   - Returns: A success message indicating that the password change request has been sent.

7. checkRestoreRequest
   - Description: Checks if a password change request exists for the given email address.
   - HTTP Method: POST
   - Endpoint: /check_restore_request
   - Parameters:
     - email: The email address of the user (string)
   - Returns: A boolean indicating whether a password change request exists or not.

8. restorePassword
   - Description: Restores the password of the user based on the password change request.
   - HTTP Method: POST
   - Endpoint: /restore_password
   - Parameters:
     - email: The email address of the user (string)
     - newPassword: The new password to be set (string)
   - Returns: A success message indicating that the password has been restored.

9. updateUser
   - Description: Updates the details of a specific user.
   - HTTP Method: PUT
   - Endpoint: /user/:id
   - Parameters:
     - id: The ID of the user to be updated (string)
     - username: The new username of the user (string)
     - password: The new password of the user (string)
   - Returns: The updated user object.

10. deleteUser
    - Description: Deletes a specific user from the database.
    - HTTP Method: DELETE
    - Endpoint: /user/:id
    - Parameters:
      - id: The ID of the user to be deleted (string)
    - Returns: A success message indicating that the user has been deleted.

Technical Concepts:
- Express.js: Express.js is a web application framework for Node.js that simplifies the process of building web applications by providing a set of robust features and utilities.
- Middleware: The `verifyToken` function is an example of middleware, which is a function that is executed before the main request handler. It is used to verify the authenticity of the token provided in the request header.

Variables Used (if applicable):
- express: The Express.js module for creating the router.
- api: The Express.js router object.
- authController: The module that handles the authentication logic.
- verifyToken: The helper function for verifying the authenticity of the token.

Template File (if applicable):
N/A
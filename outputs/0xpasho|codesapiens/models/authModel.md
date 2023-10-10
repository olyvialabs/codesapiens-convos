# authModel.js

## Description
The `authModel.js` file is a module that provides authentication and user modification functionalities. It interacts with a MySQL database using a connection pool to execute queries. The module exports an object named `authModel` that contains various methods for user authentication and management.

## Methods

### `verifyIfUserExist(email, callback)`
Verifies if a user with the specified email exists in the database.
- `email` (string): The email of the user to verify.
- `callback` (function): A callback function that will be called with the query result or an error object.

### `signup(data, callback)`
Creates a new user in the database.
- `data` (array): An array containing the user's email, name, password, and type.
- `callback` (function): A callback function that will be called with the ID of the inserted user or an error object.

### `signin(data, callback)`
Authenticates a user by checking their email and password in the database.
- `data` (array): An array containing the user's email and password.
- `callback` (function): A callback function that will be called with the user's data or an error object.

### `getAllUsers(data, callback)`
Retrieves a list of all users from the database, with optional pagination and search functionality.
- `data` (object): An object containing the page number, page length, and search keyword.
- `callback` (function): A callback function that will be called with the query result or an error object.

### `updateUser(data, callback)`
Updates a user's information in the database, excluding the password.
- `data` (array): An array containing the user's name, email, type, and ID.
- `callback` (function): A callback function that will be called with the query result or an error object.

### `updateUserWithPassword(data, callback)`
Updates a user's information in the database, including the password.
- `data` (array): An array containing the user's name, email, type, password, and ID.
- `callback` (function): A callback function that will be called with the query result or an error object.

### `deleteUser(id, callback)`
Soft deletes a user by setting their status to 0 in the database.
- `id` (number): The ID of the user to delete.
- `callback` (function): A callback function that will be called with the query result or an error object.

### `getUserData(id, callback)`
Retrieves the user's name and type (level) using the provided ID.
- `id` (number): The ID of the user to retrieve data for.
- `callback` (function): A callback function that will be called with the user's data or an error object.

### `changePassword(data, callback)`
Changes the user's password using the provided ID and new password.
- `data` (object): An object containing the user's ID and new password.
- `callback` (function): A callback function that will be called with the query result or an error object.

### `registerRestoreRequest(iduser, callback)`
Adds a restore password request to the database for the specified user.
- `iduser` (number): The ID of the user requesting a password restore.
- `callback` (function): A callback function that will be called with the ID of the inserted restore request or an error object.

### `checkRestoreRequest(idrestorepassword, callback)`
Checks if a restore password request exists in the database.
- `idrestorepassword` (number): The ID of the restore password log to check.
- `callback` (function): A callback function that will be called with the restore request data or an error object.

### `setPasswordRestored(idrestorepassword, callback)`
Marks a restore password request as taken in the database.
- `idrestorepassword` (number): The ID of the restore password log to mark as taken.
- `callback` (function): A callback function that will be called with the query result or an error object.

## Technical Concepts
- Connection Pool: The module uses a connection pool to manage database connections efficiently. A connection pool is a cache of database connections maintained so that the connections can be reused when needed, rather than creating a new connection every time a request is made.
- SHA: The module uses the SHA hashing algorithm to securely store and compare passwords. SHA (Secure Hash Algorithm) is a cryptographic hash function that takes an input and produces a fixed-size string of characters, which is typically a hexadecimal representation of the hash value.

## Example Usage
```javascript
const authModel = require('./authModel');

// Example usage of verifyIfUserExist method
authModel.verifyIfUserExist('example@example.com', (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});

// Example usage of signup method
const userData = ['example@example.com', 'John Doe', 'password123', 1];
authModel.signup(userData, (insertId, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(`User created with ID: ${insertId}`);
  }
});

// Example usage of signin method
const loginData = ['example@example.com', 'password123'];
authModel.signin(loginData, (user, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(user);
  }
});

// Example usage of getAllUsers method
const searchData = { page: 1, pageLength: 10, search: 'example' };
authModel.getAllUsers(searchData, (users, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(users);
  }
});

// Example usage of updateUser method
const updateData = ['John Doe', 'newemail@example.com', 2, 1];
authModel.updateUser(updateData, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});

// Example usage of updateUserWithPassword method
const updateDataWithPassword = ['John Doe', 'newemail@example.com', 2, 'newpassword123', 1];
authModel.updateUserWithPassword(updateDataWithPassword, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});

// Example usage of deleteUser method
const userId = 1;
authModel.deleteUser(userId, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});

// Example usage of getUserData method
const userIdToRetrieve = 1;
authModel.getUserData(userIdToRetrieve, (user, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(user);
  }
});

// Example usage of changePassword method
const passwordData = { iduser: 1, newPassword: 'newpassword123' };
authModel.changePassword(passwordData, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});

// Example usage of registerRestoreRequest method
const restoreUserId = 1;
authModel.registerRestoreRequest(restoreUserId, (insertId, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(`Restore request created with ID: ${insertId}`);
  }
});

// Example usage of checkRestoreRequest method
const restoreRequestId = 1;
authModel.checkRestoreRequest(restoreRequestId, (restoreRequest, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(restoreRequest);
  }
});

// Example usage of setPasswordRestored method
const restoreRequestIdToMark = 1;
authModel.setPasswordRestored(restoreRequestIdToMark, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

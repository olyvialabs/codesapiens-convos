# departmentController.js

## Description
The `departmentController.js` file is a JavaScript module that contains functions for handling department-related operations in a database. It exports several methods that can be used to insert, retrieve, update, and delete department data.

## Examples
Here are some examples of how to use the `departmentController.js` module:

1. Retrieving all departments in the database:
```javascript
const departmentController = require("./departmentController");

departmentController.getDepartments(request, response, next);
```

2. Inserting a new department into the database:
```javascript
const departmentController = require("./departmentController");

const departmentData = {
  name: "Marketing",
};

departmentController.insertDepartment(request, response, next);
```

3. Updating a department's data in the database:
```javascript
const departmentController = require("./departmentController");

const departmentId = 1;
const departmentData = {
  name: "Sales",
};

departmentController.updateDepartment(request, response, next);
```

4. Deleting a department from the database:
```javascript
const departmentController = require("./departmentController");

const departmentId = 1;

departmentController.deleteDepartment(request, response, next);
```

## Methods

### getDepartments(request, response, next)
Retrieves all departments in the database.

- Parameters:
  - `request` (Object): JSON object that contains all the information from the `GET` request.
  - `response` (Object): Server response to the final user.
  - `next` (function): Express method that jumps into the next route function.

### insertDepartment(request, response, next)
Inserts a new department into the database.

- Parameters:
  - `request` (Object): JSON object that contains all the information from the `GET` request.
  - `response` (Object): Server response to the final user.
  - `next` (function): Express method that jumps into the next route function.

### updateDepartment(request, response, next)
Updates a department's data in the database.

- Parameters:
  - `request` (Object): JSON object that contains all the information from the `GET` request.
  - `response` (Object): Server response to the final user.
  - `next` (function): Express method that jumps into the next route function.

### deleteDepartment(request, response, next)
Deletes a department from the database.

- Parameters:
  - `request` (Object): JSON object that contains all the information from the `DELETE` request.
  - `response` (Object): Server response to the final user.
  - `next` (function): Express method that jumps into the next route function.

## Technical Concepts

### JSON Web Token (JWT)
The `jwt` module is used to handle JSON Web Tokens, which are used for authentication and authorization purposes. It provides functions for generating, signing, and verifying tokens. In this file, the `jwt` module is used to sign and verify tokens using a secret key stored in the `JWT_SECRET` environment variable.

## Dependencies

### jwt
The `jwt` module is a dependency required for handling JSON Web Tokens.

### departmentModel
The `departmentModel` module is a dependency required for interacting with the department data in the database.

## Usage
To use the `departmentController.js` module, require it in your JavaScript file and call the desired methods with the appropriate parameters. Make sure to have the required dependencies installed and configured properly.

```javascript
const departmentController = require("./departmentController");

// Call the desired methods
departmentController.getDepartments(request, response, next);
departmentController.insertDepartment(request, response, next);
departmentController.updateDepartment(request, response, next);
departmentController.deleteDepartment(request, response, next);
```

Remember to replace `request`, `response`, and `next` with the actual objects and functions from your application.
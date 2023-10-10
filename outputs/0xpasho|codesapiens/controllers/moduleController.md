# moduleController.js

## Description
The `moduleController.js` file is a JavaScript file that contains the controller functions for managing modules in a database. It exports four functions: `addModule`, `getAllModules`, `updateModule`, and `deleteModule`. These functions interact with the `moduleModel` module to perform CRUD operations on the modules.

## Examples
Here are some examples of how to use the `moduleController.js` class:

1. Adding a module:
```javascript
const request = { body: { name: 'Module 1', best_practices: 'Some best practices', all_companies_average: 85 } };
const response = { send: (data) => console.log(data) };
const next = (error) => console.error(error);

addModule(request, response, next);
```

2. Getting all modules:
```javascript
const request = { query: { search: 'Module' } };
const response = { send: (data) => console.log(data) };
const next = (error) => console.error(error);

getAllModules(request, response, next);
```

3. Updating a module:
```javascript
const request = { params: { idmodule: 1 }, body: { name: 'Updated Module', best_practices: 'Updated best practices', all_companies_average: 90 } };
const response = { send: (data) => console.log(data) };
const next = (error) => console.error(error);

updateModule(request, response, next);
```

4. Deleting a module:
```javascript
const request = { params: { idmodule: 1 } };
const response = { send: (data) => console.log(data) };
const next = (error) => console.error(error);

deleteModule(request, response, next);
```

## Methods

### addModule(request, response, next)
Adds a module to the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### getAllModules(request, response, next)
Gets all the modules from the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### updateModule(request, response, next)
Updates a module's information in the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### deleteModule(request, response, next)
Updates a module's status to zero in the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

## Technical Concepts
There are no specific technical concepts in this file.
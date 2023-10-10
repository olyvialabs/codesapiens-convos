# formActionController.js

## Description
The `formActionController.js` file is a JavaScript module that contains functions for handling form actions in a web application. It exports several methods that interact with a database model to perform CRUD (Create, Read, Update, Delete) operations on form actions. These methods are used as route handlers in an Express.js application.

## Examples
Here are some examples of how to use the `formActionController` class:

```javascript
const formActionController = require('./formActionController');

// Example 1: Adding a new form action
const request = {
  body: {
    idform: 1,
    x_position: 100,
    y_position: 200,
    information: 'Submit form'
  }
};
const response = {
  send: function(data) {
    console.log(data);
  },
  status: function(code) {
    return this;
  },
  send: function(data) {
    console.log(data);
  }
};
const next = function(error) {
  console.error(error);
};

formActionController.addFormAction(request, response, next);

// Example 2: Getting all form actions of a specific form
const request = {
  params: {
    idform: 1
  }
};
const response = {
  send: function(data) {
    console.log(data);
  }
};
const next = function(error) {
  console.error(error);
};

formActionController.getAllFormActions(request, response, next);

// Example 3: Updating a form action information
const request = {
  params: {
    idaction: 1
  },
  body: {
    information: 'Updated form action'
  }
};
const response = {
  status: function(code) {
    return this;
  },
  send: function(data) {
    console.log(data);
  }
};
const next = function(error) {
  console.error(error);
};

formActionController.updateFormActions(request, response, next);

// Example 4: Deleting a form action
const request = {
  params: {
    idaction: 1
  }
};
const response = {
  status: function(code) {
    return this;
  },
  send: function(data) {
    console.log(data);
  }
};
const next = function(error) {
  console.error(error);
};

formActionController.deleteFormAction(request, response, next);
```

## Methods

### addFormAction(request, response, next)
Adds a new form action in the database.

Parameters:
- `request` (object): JSON object that contains all the information from the `POST` request.
  - `request.body` (object): Data sent from the client.
    - `request.body.idform` (number): Form ID.
    - `request.body.x_position` (number): X position.
    - `request.body.y_position` (number): Y position.
    - `request.body.information` (string): Form action information.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### getAllFormActions(request, response, next)
Gets all the actions of a specific form from the database.

Parameters:
- `request` (object): JSON object that contains all the information from the `GET` request.
  - `request.params` (object): Request parameters.
    - `request.params.idform` (number): Form ID.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### updateFormActions(request, response, next)
Updates a form action information in the database.

Parameters:
- `request` (object): JSON object that contains all the information from the `PUT` request.
  - `request.params` (object): Request parameters.
    - `request.params.idaction` (number): Form action ID.
  - `request.body` (object): Data sent from the client.
    - `request.body.information` (string): Form action information.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### deleteFormAction(request, response, next)
Updates a form action status to zero in the database.

Parameters:
- `request` (object): JSON object that contains all the information from the `DELETE` request.
  - `request.params` (object): Request parameters.
    - `request.params.idaction` (number): Form action ID.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

## Technical Concepts
- Express.js: Express.js is a web application framework for Node.js that provides a set of features for building web applications and APIs.
- JSON: JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. It is a standard data format that uses key-value pairs to represent data objects.
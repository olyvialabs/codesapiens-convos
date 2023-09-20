# formActionController.js

This file contains the implementation of the form action controller, which is responsible for handling form action-related requests and interacting with the form action model.

## Examples

Here are some examples of how to use the form action controller:

1. Adding a new form action:
```javascript
const request = {
  body: {
    idform: 1,
    x_position: 100,
    y_position: 200,
    information: "Sample form action"
  }
};

const response = {
  send: (data) => {
    console.log(data);
  },
  status: (code) => {
    return {
      send: (error) => {
        console.error(error);
      }
    };
  }
};

const next = (error) => {
  console.error(error);
};

addFormAction(request, response, next);
```

2. Getting all actions of a specific form:
```javascript
const request = {
  params: {
    idform: 1
  }
};

const response = {
  send: (data) => {
    console.log(data);
  }
};

const next = (error) => {
  console.error(error);
};

getAllFormActions(request, response, next);
```

3. Updating a form action information:
```javascript
const request = {
  params: {
    idaction: 1
  },
  body: {
    information: "Updated form action"
  }
};

const response = {
  send: (data) => {
    console.log(data);
  },
  status: (code) => {
    return {
      send: (error) => {
        console.error(error);
      }
    };
  }
};

const next = (error) => {
  console.error(error);
};

updateFormActions(request, response, next);
```

4. Deleting a form action:
```javascript
const request = {
  params: {
    idaction: 1
  }
};

const response = {
  send: (data) => {
    console.log(data);
  },
  status: (code) => {
    return {
      send: (error) => {
        console.error(error);
      }
    };
  }
};

const next = (error) => {
  console.error(error);
};

deleteFormAction(request, response, next);
```

## Methods

### addFormAction(request, response, next)
Adds a new form action in the database.

- `request` (object): JSON that contains all the information from the `POST` request.
  - `request.body` (object): Data sent from the client.
    - `request.body.idform` (number): Form ID.
    - `request.body.x_position` (number): X position.
    - `request.body.y_position` (number): Y position.
    - `request.body.information` (string): Form action information.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### getAllFormActions(request, response, next)
Gets all the actions of a specific form.

- `request` (object): JSON that contains all the information from the `GET` request.
  - `request.params` (object): Request parameters.
    - `request.params.idform` (number): Form ID.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### updateFormActions(request, response, next)
Updates a form action information in the database.

- `request` (object): JSON that contains all the information from the `PUT` request.
  - `request.params` (object): Request parameters.
    - `request.params.idaction` (number): Form action ID.
  - `request.body` (object): Data sent from the client.
    - `request.body.information` (string): Form action information.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### deleteFormAction(request, response, next)
Updates a form action status to zero.

- `request` (object): JSON that contains all the information from the `DELETE` request.
  - `request.params` (object): Request parameters.
    - `request.params.idaction` (number): Form action ID.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

## Technical Concepts

- Express: Express is a popular web application framework for Node.js. It provides a set of features for building web applications and APIs, including routing, middleware, and request/response handling.
- JSON: JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. It is often used for transmitting data between a server and a web application, as well as storing configuration or data files.

---

Please note that this documentation assumes familiarity with JavaScript, Node.js, and Express.
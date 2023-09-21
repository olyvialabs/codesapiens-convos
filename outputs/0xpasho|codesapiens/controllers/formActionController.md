# formActionController.js

## Description
The `formActionController.js` file is a JavaScript module that contains functions for handling form actions in a web application. It exports several methods that interact with the `formActionModel` module to perform CRUD operations on form actions in a database. This file is typically used as a controller in an Express.js application.

## Examples
Here are some examples of how to use the `formActionController` class:

1. Adding a new form action:
```javascript
const request = {
  body: {
    idform: 1,
    x_position: 100,
    y_position: 200,
    information: "Submit form"
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

const next = () => {
  console.log("Next route function");
};

formActionController.addFormAction(request, response, next);
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

const next = () => {
  console.log("Next route function");
};

formActionController.getAllFormActions(request, response, next);
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

const next = () => {
  console.log("Next route function");
};

formActionController.updateFormActions(request, response, next);
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

const next = () => {
  console.log("Next route function");
};

formActionController.deleteFormAction(request, response, next);
```

## Methods

### addFormAction(request, response, next)
Adds a new form action in the database.

#### Parameters
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

#### Parameters
- `request` (object): JSON that contains all the information from the `GET` request.
  - `request.params` (object): Request parameters.
    - `request.params.idform` (number): Form ID.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### updateFormActions(request, response, next)
Updates a form action information in the database.

#### Parameters
- `request` (object): JSON that contains all the information from the `PUT` request.
  - `request.params` (object): Request parameters.
    - `request.params.idaction` (number): Form action ID.
  - `request.body` (object): Data sent from the client.
    - `request.body.information` (string): Form action information.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

### deleteFormAction(request, response, next)
Updates a form action status to zero.

#### Parameters
- `request` (object): JSON that contains all the information from the `DELETE` request.
  - `request.params` (object): Request parameters.
    - `request.params.idaction` (number): Form action ID.
- `response` (object): Server response to the final user.
- `next` (function): Express method that jumps into the next route function.

## Technical Concepts
- Express.js: Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.
- JSON: JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. It is based on a subset of the JavaScript Programming Language Standard ECMA-262 3rd Edition - December 1999. JSON is a text format that is completely language independent but uses conventions that are familiar to programmers of the C-family of languages, including C, C++, C#, Java, JavaScript, Perl, Python, and many others. These properties make JSON an ideal data-interchange language.
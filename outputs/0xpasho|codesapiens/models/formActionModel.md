# formActionModel.js

## Description
The `formActionModel.js` file is a module that manages form actions in a database. It provides methods to add, retrieve, update, and delete form actions. The module uses a MySQL database connection pool to execute SQL queries.

## Code Examples
Here are some examples of how to use the `formActionModel` class:

1. Adding a form action:
```javascript
const formActionModel = require('formActionModel');

const data = {
  idform: 1,
  x_position: 100,
  y_position: 200,
  information: 'Submit form'
};

formActionModel.addFormAction(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log('Form action added successfully');
  }
});
```

2. Retrieving all form actions for a specific form:
```javascript
const formActionModel = require('formActionModel');

const idform = 1;

formActionModel.getAllFormActions(idform, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

3. Updating a form action information:
```javascript
const formActionModel = require('formActionModel');

const data = {
  idaction: 1,
  information: 'Updated form action'
};

formActionModel.updateFormActions(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log('Form action updated successfully');
  }
});
```

4. Deleting a form action:
```javascript
const formActionModel = require('formActionModel');

const idaction = 1;

formActionModel.deleteFormAction(idaction, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log('Form action deleted successfully');
  }
});
```

## Methods

### makeQuery(query, data, callback)
Makes a SQL query to the database.

- `query` (string): The SQL query string.
- `data` (array): An array of ordered values that will be inserted into the query.
- `callback` (function): A callback function that returns the result or error of the query.

### formActionModel.addFormAction(data, callback)
Adds a form action to the database.

- `data` (object): The form action data.
  - `idform` (number): The ID of the form.
  - `x_position` (number): The X position of the form action.
  - `y_position` (number): The Y position of the form action.
  - `information` (string): The information of the form action.
- `callback` (function): A callback function that returns the result or error of the query.

### formActionModel.getAllFormActions(idform, callback)
Gets all the actions of a specific form from the database.

- `idform` (number): The ID of the form.
- `callback` (function): A callback function that returns the result or error of the query.

### formActionModel.updateFormActions(data, callback)
Updates a form action information in the database.

- `data` (object): The form action data.
  - `idaction` (number): The ID of the form action.
  - `information` (string): The updated information of the form action.
- `callback` (function): A callback function that returns the result or error of the query.

### formActionModel.deleteFormAction(idaction, callback)
Updates a form action status to zero in the database.

- `idaction` (number): The ID of the form action.
- `callback` (function): A callback function that returns the result or error of the query.

## Technical Concepts

### MySQL Connection Pool
The `formActionModel` module uses a MySQL connection pool to manage database connections efficiently. A connection pool is a cache of database connections maintained so that the connections can be reused when needed. It helps improve performance by reducing the overhead of establishing a new connection for each query.

The `pool` object is imported from the `mysqlPool` module and is used to acquire and release connections from the pool. The `getConnection` method is used to get a connection from the pool, and the `release` method is used to release the connection back to the pool after the query is executed.

## Template Variables
N/A (This is not a template file)

## File Content
The `formActionModel.js` file exports an object named `formActionModel` that contains methods for managing form actions in a database. The file starts with the required import of the `pool` object from the `mysqlPool` module.

The `formActionModel` object is then defined and initialized as an empty object.

The file also defines a callback type named `ResponseCallback`, which is used to handle the result or error of a database query.

The `makeQuery` function is defined, which takes a query string, an array of data values, and a callback function as parameters. This function is responsible for executing the SQL query using the connection pool and returning the result or error to the callback function.

The `formActionModel` object's methods are then defined using arrow function syntax. Each method takes specific parameters and calls the `makeQuery` function with the appropriate SQL query and data values.

Finally, the `formActionModel` object is exported from the module to make it accessible to other parts of the application.
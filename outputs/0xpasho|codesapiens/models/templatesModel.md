# templatesModel.js

## Description
The `templatesModel.js` file is a module that provides methods for interacting with the `template` table in a MySQL database. It uses a connection pool from the `mysqlPool` module to handle database connections.

## Methods

### getTemplatesLength(callback)
This method retrieves the number of templates in the database that have a status of 1 (active).

#### Parameters
- `callback`: A callback function that will be called with the result or an error. The callback function should accept two parameters: `error` and `result`.

### getTemplates(data, callback)
This method retrieves a subset of templates from the database based on the provided data.

#### Parameters
- `data`: An object containing the following properties:
  - `searchQuery` (optional): A string representing a search query to filter the templates by name.
  - `tablePage`: A number representing the current page of the table.
  - `tableDisplayLength`: A number representing the number of templates to display per page.
- `callback`: A callback function that will be called with the result or an error. The callback function should accept two parameters: `error` and `result`.

### insertTemplate(data, callback)
This method inserts a new template into the database.

#### Parameters
- `data`: An object containing the following properties:
  - `name`: A string representing the name of the template.
  - `options`: An object representing the options of the template.
- `callback`: A callback function that will be called with the result or an error. The callback function should accept two parameters: `error` and `result`.

### getTemplate(data, callback)
This method retrieves a single template from the database based on the provided template ID.

#### Parameters
- `data`: An object containing the following properties:
  - `id`: A number representing the ID of the template to retrieve.
- `callback`: A callback function that will be called with the result or an error. The callback function should accept two parameters: `error` and `result`.

### updateTemplate(data, callback)
This method updates an existing template in the database.

#### Parameters
- `data`: An object containing the following properties:
  - `name`: A string representing the updated name of the template.
  - `options`: An object representing the updated options of the template.
  - `id`: A number representing the ID of the template to update.
- `callback`: A callback function that will be called with the result or an error. The callback function should accept two parameters: `error` and `result`.

### deleteTemplate(data, callback)
This method marks a template as deleted in the database by setting its status to 0.

#### Parameters
- `data`: An object containing the following properties:
  - `id`: A number representing the ID of the template to delete.
- `callback`: A callback function that will be called with the result or an error. The callback function should accept two parameters: `error` and `result`.

## Technical Concepts
- Connection Pool: The `pool` object is used to manage a pool of database connections. It allows for efficient reuse of connections and helps prevent connection leaks.
- Callback Functions: The methods in this module accept callback functions as parameters. These functions are called asynchronously with the result or an error once the database operation is complete.

## Examples
Here are some examples of how to use the `templatesModel` module:

### Example 1: Retrieving the number of templates
```javascript
const templatesModel = require('templatesModel');

templatesModel.getTemplatesLength((error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

### Example 2: Retrieving a subset of templates
```javascript
const templatesModel = require('templatesModel');

const data = {
  searchQuery: 'example',
  tablePage: 1,
  tableDisplayLength: 10
};

templatesModel.getTemplates(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

### Example 3: Inserting a new template
```javascript
const templatesModel = require('templatesModel');

const data = {
  name: 'New Template',
  options: { option1: 'value1', option2: 'value2' }
};

templatesModel.insertTemplate(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

### Example 4: Retrieving a single template
```javascript
const templatesModel = require('templatesModel');

const data = {
  id: 1
};

templatesModel.getTemplate(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

### Example 5: Updating an existing template
```javascript
const templatesModel = require('templatesModel');

const data = {
  name: 'Updated Template',
  options: { option1: 'new value1', option2: 'new value2' },
  id: 1
};

templatesModel.updateTemplate(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

### Example 6: Deleting a template
```javascript
const templatesModel = require('templatesModel');

const data = {
  id: 1
};

templatesModel.deleteTemplate(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```
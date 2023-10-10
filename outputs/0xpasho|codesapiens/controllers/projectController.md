# projectController.js

## Description
The `projectController.js` file is a JavaScript file that contains functions for handling project-related requests. It interacts with the `projectModel` module to perform CRUD operations on project data.

## Examples
Here are some examples of how to use the `projectController.js` class:

1. Get a specific project:
```javascript
GET /projects/123
```

2. Get a list of projects with pagination and search:
```javascript
GET /projects?searchProject=example&tablePage=1&tableDisplayLength=10
```

3. Insert a new project:
```javascript
POST /projects
{
  "name": "New Project",
  "description": "This is a new project",
  "idcompany": 456
}
```

4. Update an existing project:
```javascript
PUT /projects/123
{
  "name": "Updated Project",
  "description": "This project has been updated"
}
```

5. Delete a project:
```javascript
DELETE /projects/123
```

## Methods

### getProject(request, response, next)
This method is used to retrieve project data. It can be used to get a specific project by providing the project ID as a parameter, or to get a list of projects with pagination and search options.

Parameters:
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

### insertProject(request, response, next)
This method is used to insert a new project into the database.

Parameters:
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

### updateProject(request, response, next)
This method is used to update an existing project in the database.

Parameters:
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

### deleteProject(request, response, next)
This method is used to delete a project from the database.

Parameters:
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## Technical Concepts
- `projectModel`: This is a module that handles database operations related to projects. It is required at the beginning of the file using `require('../models/projectModel')`.
- `request.params`: This object contains the parameters extracted from the URL path.
- `request.query`: This object contains the query parameters extracted from the URL.
- `response.status(200)`: This sets the HTTP status code of the response to 200 (OK).
- `response.send()`: This sends the response data back to the client.

## Example Usage
```javascript
const projectController = require('./projectController');

// Get a specific project
projectController.getProject(req, res, next);

// Insert a new project
projectController.insertProject(req, res, next);

// Update an existing project
projectController.updateProject(req, res, next);

// Delete a project
projectController.deleteProject(req, res, next);
```

## Exported Functions
The following functions are exported from the `projectController.js` file:

- `getProject`: Retrieves project data.
- `insertProject`: Inserts a new project into the database.
- `updateProject`: Updates an existing project in the database.
- `deleteProject`: Deletes a project from the database.
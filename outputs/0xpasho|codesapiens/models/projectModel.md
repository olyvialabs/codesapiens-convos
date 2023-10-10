# projectModel.js

## Description
The `projectModel.js` file is a module that contains methods for interacting with the `project` table in a MySQL database. It provides functions for retrieving, inserting, updating, and deleting projects.

## Usage Examples
Before diving into the details of each method, here are some examples of how to use the `projectModel` class:

1. Get the total number of projects:
```javascript
projectModel.getProjectsLength((error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

2. Get a list of projects with pagination and search functionality:
```javascript
const data = {
  searchProject: 'example',
  tablePage: 1,
  tableDisplayLength: 10
};

projectModel.getProjects(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

3. Get a specific project by its ID:
```javascript
const data = {
  idproject: 1
};

projectModel.getProject(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

4. Insert a new project:
```javascript
const data = {
  name: 'New Project',
  description: 'This is a new project'
};

projectModel.insertProject(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

5. Update an existing project:
```javascript
const data = {
  name: 'Updated Project',
  description: 'This project has been updated',
  idproject: 1
};

projectModel.updateProject(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

6. Delete a project:
```javascript
const data = {
  idproject: 1
};

projectModel.deleteProject(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

## Methods

### getProjectsLength(callback)
Retrieves the total number of projects in the database.

Parameters:
- `callback` (function): A callback function that will be called with the result or an error object.

### getProjects(data, callback)
Retrieves a list of projects from the database.

Parameters:
- `data` (object): An object containing the following properties:
  - `searchProject` (string, optional): A search term to filter projects by name, description, or creation date.
  - `tablePage` (number): The current page number for pagination.
  - `tableDisplayLength` (number): The number of projects to display per page.
- `callback` (function): A callback function that will be called with the result or an error object.

### getProject(data, callback)
Retrieves a specific project from the database by its ID.

Parameters:
- `data` (object): An object containing the following properties:
  - `idproject` (number): The ID of the project to retrieve.
- `callback` (function): A callback function that will be called with the result or an error object.

### insertProject(data, callback)
Inserts a new project into the database.

Parameters:
- `data` (object): An object containing the following properties:
  - `name` (string): The name of the project.
  - `description` (string): The description of the project.
- `callback` (function): A callback function that will be called with the result or an error object.

### insertProjectRelation(data, callback)
Inserts a new relation between a company and a project into the database.

Parameters:
- `data` (object): An object containing the following properties:
  - `idcompany` (number): The ID of the company.
  - `idproject` (number): The ID of the project.
- `callback` (function): A callback function that will be called with the result or an error object.

### updateProject(data, callback)
Updates an existing project in the database.

Parameters:
- `data` (object): An object containing the following properties:
  - `name` (string): The updated name of the project.
  - `description` (string): The updated description of the project.
  - `idproject` (number): The ID of the project to update.
- `callback` (function): A callback function that will be called with the result or an error object.

### deleteProject(data, callback)
Deletes a project from the database.

Parameters:
- `data` (object): An object containing the following properties:
  - `idproject` (number): The ID of the project to delete.
- `callback` (function): A callback function that will be called with the result or an error object.

## Technical Concepts
- `pool`: The `pool` object is imported from the `mysqlPool` module and represents a connection pool to the MySQL database. It is used to manage and reuse database connections efficiently.
- `connection`: The `connection` object represents a single connection to the MySQL database. It is obtained from the connection pool and should be released after use to free up resources.

## Note
This file assumes the existence of a `project` table in the database, which has the following columns:
- `idproject` (number): The unique ID of the project.
- `name` (string): The name of the project.
- `description` (string): The description of the project.
- `creation_date` (date): The date when the project was created.

The file also assumes the existence of a `form_project` table and a `company_project` table, which are used for relations with projects.
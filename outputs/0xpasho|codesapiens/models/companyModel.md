# companyModel.js

## Description
The `companyModel.js` file is a module that contains methods for interacting with the `company` table in a MySQL database. It provides functions for retrieving, inserting, updating, and deleting company data.

## Examples
Before diving into the details of each method, here are some examples of how to use the `companyModel` class:

1. Get the total number of companies:
```javascript
companyModel.getCompaniesLength((error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

2. Get a list of companies with pagination and search functionality:
```javascript
const data = {
  searchCompany: 'example',
  tablePage: 1,
  tableDisplayLength: 10
};

companyModel.getCompanies(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

3. Get a specific company by ID:
```javascript
const data = {
  idcompany: 1
};

companyModel.getCompany(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

4. Insert a new company:
```javascript
const data = {
  name: 'Example Company',
  description: 'This is an example company.'
};

companyModel.insertCompany(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

5. Update an existing company:
```javascript
const data = {
  name: 'Updated Company',
  description: 'This company has been updated.',
  idcompany: 1
};

companyModel.updateCompany(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

6. Update the image of a company:
```javascript
const data = {
  image: 'example.jpg',
  idcompany: 1
};

companyModel.updateCompanyImage(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

7. Delete a company:
```javascript
const data = {
  idcompany: 1
};

companyModel.deleteCompany(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

## Methods

### getCompaniesLength(callback)
Retrieves the total number of companies in the database.

- Parameters:
  - `callback` (function): A callback function that will be called with the result or an error.

### getCompanies(data, callback)
Retrieves a list of companies from the database with pagination and search functionality.

- Parameters:
  - `data` (object): An object containing the following properties:
    - `searchCompany` (string, optional): A search term to filter the companies by name, description, or creation date.
    - `tablePage` (number): The current page number.
    - `tableDisplayLength` (number): The number of companies to display per page.
  - `callback` (function): A callback function that will be called with the result or an error.

### getCompany(data, callback)
Retrieves a specific company from the database by ID.

- Parameters:
  - `data` (object): An object containing the following properties:
    - `idcompany` (number): The ID of the company to retrieve.
  - `callback` (function): A callback function that will be called with the result or an error.

### insertCompany(data, callback)
Inserts a new company into the database.

- Parameters:
  - `data` (object): An object containing the following properties:
    - `name` (string): The name of the company.
    - `description` (string): The description of the company.
  - `callback` (function): A callback function that will be called with the result or an error.

### updateCompany(data, callback)
Updates an existing company in the database.

- Parameters:
  - `data` (object): An object containing the following properties:
    - `name` (string): The updated name of the company.
    - `description` (string): The updated description of the company.
    - `idcompany` (number): The ID of the company to update.
  - `callback` (function): A callback function that will be called with the result or an error.

### updateCompanyImage(data, callback)
Updates the image of a company in the database.

- Parameters:
  - `data` (object): An object containing the following properties:
    - `image` (string): The updated image URL of the company.
    - `idcompany` (number): The ID of the company to update.
  - `callback` (function): A callback function that will be called with the result or an error.

### deleteCompany(data, callback)
Deletes a company from the database.

- Parameters:
  - `data` (object): An object containing the following properties:
    - `idcompany` (number): The ID of the company to delete.
  - `callback` (function): A callback function that will be called with the result or an error.

## Technical Concepts
- `pool`: The `pool` object is used to manage connections to the MySQL database. It is imported from the `mysqlPool` module.
- `getConnection`: The `getConnection` method is used to get a connection from the connection pool. It takes a callback function as a parameter, which will be called with the connection object.
- `query`: The `query` method is used to execute SQL queries on the database. It takes the SQL query as a parameter and a callback function, which will be called with the result or an error.
- `connection.release()`: The `release` method is used to release the connection back to the connection pool after it has been used.


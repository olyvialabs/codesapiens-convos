# companyController.js

## Description

The `companyController.js` file is a module that contains functions for handling company-related operations. It interacts with the `companyModel` module to perform CRUD (Create, Read, Update, Delete) operations on company data. Additionally, it provides functionality for managing company images.

## Examples

Before diving into the details of each method, let's look at some examples of how to use the `companyController` class:

1. Example 1: Get a list of companies with pagination and search filters:
```javascript
GET /companies?searchCompany=example&tablePage=1&tableDisplayLength=10
```

2. Example 2: Get a specific company by ID:
```javascript
GET /companies/123
```

3. Example 3: Insert a new company:
```javascript
POST /companies
Body: {
  "name": "Example Company",
  "description": "This is an example company"
}
```

4. Example 4: Update an existing company:
```javascript
PUT /companies/123
Body: {
  "name": "Updated Company",
  "description": "This is the updated description"
}
```

5. Example 5: Delete a company:
```javascript
DELETE /companies/123
```

6. Example 6: Set a company image:
```javascript
POST /companies/123/image
Body: [multipart/form-data] - file upload
```

7. Example 7: Get a company image:
```javascript
GET /companies/123/image
```

## Methods

### getCompany(request, response, next)

This method retrieves company data based on the provided parameters. If an `id` parameter is provided, it fetches a specific company by ID. Otherwise, it returns a list of companies with pagination and search filters.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### insertCompany(request, response, next)

This method inserts a new company into the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### updateCompany(request, response, next)

This method updates an existing company in the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### deleteCompany(request, response, next)

This method deletes a company from the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### setCompanyImage(request, response, next)

This method sets the image for a company. It handles file upload and updates the company's image path in the database.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

### getCompanyImage(request, response, next)

This method retrieves the image for a company based on the company ID. If the image exists, it sends the image file. Otherwise, it returns a 404 error.

Parameters:
- `request` (object): The HTTP request object.
- `response` (object): The HTTP response object.
- `next` (function): The next middleware function.

## Technical Concepts

### File System (fs)

The `fs` module is a built-in Node.js module that provides an API for interacting with the file system. In this file, it is used for renaming and deleting temporary image files.

### Path (path)

The `path` module is another built-in Node.js module that provides utilities for working with file and directory paths. It is used in this file to manipulate file paths and join directory paths.

## Variables

The `companyController.js` file does not define any variables.

## Template File

This file does not contain a template.
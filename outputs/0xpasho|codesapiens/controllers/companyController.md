# companyController.js

The `companyController.js` file contains the implementation of various functions that handle requests related to company data. These functions interact with the `companyModel` module to perform CRUD operations on the company data.

## Examples

Before diving into the details of each function, let's look at some examples of how to use the `companyController` class:

1. Example of getting a company by ID:
```javascript
GET /companies/123
```

2. Example of getting a list of companies with pagination and search:
```javascript
GET /companies?searchCompany=example&tablePage=1&tableDisplayLength=10
```

3. Example of inserting a new company:
```javascript
POST /companies
{
  "name": "Example Company",
  "description": "This is an example company"
}
```

4. Example of updating an existing company:
```javascript
PUT /companies/123
{
  "name": "Updated Company",
  "description": "This is an updated company"
}
```

5. Example of deleting a company:
```javascript
DELETE /companies/123
```

6. Example of setting a company image:
```javascript
POST /companies/123/image
```
*Request body should contain the image file*

7. Example of getting a company image:
```javascript
GET /companies/123/image
```

## getCompany(request, response, next)

This function retrieves company data based on the provided parameters. If an `id` parameter is present, it retrieves a single company by ID. If the `id` parameter is not present, it retrieves a list of companies with pagination and search options.

### Parameters
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## insertCompany(request, response, next)

This function inserts a new company into the database.

### Parameters
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## updateCompany(request, response, next)

This function updates an existing company in the database.

### Parameters
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## deleteCompany(request, response, next)

This function deletes a company from the database.

### Parameters
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## setCompanyImage(request, response, next)

This function sets the image of a company. It saves the image file to the server and updates the company's image path in the database.

### Parameters
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## getCompanyImage(request, response, next)

This function retrieves the image of a company.

### Parameters
- `request`: The HTTP request object.
- `response`: The HTTP response object.
- `next`: The next middleware function.

## Technical Concepts

### fs (File System)

The `fs` module is a built-in Node.js module that provides an API for interacting with the file system. In this file, it is used to perform operations such as renaming and deleting files.

### path

The `path` module is a built-in Node.js module that provides utilities for working with file and directory paths. In this file, it is used to manipulate file paths and join directory paths.

## Conclusion

The `companyController.js` file contains functions that handle various operations related to company data. These functions can be used to retrieve, insert, update, and delete company records in the database. Additionally, there are functions to set and retrieve company images. The file makes use of the `companyModel` module to interact with the database.
departmentModel.js

Description:
This file contains the code for interacting with the "department" table in the database. It provides various methods for retrieving, inserting, updating, and deleting department records.

Examples of how to use this class:

Example 1: Get the number of departments
```
const departmentModel = require('./departmentModel');

departmentModel.getDepartmentsLength((error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Example 2: Get a department by name
```
const departmentModel = require('./departmentModel');

const name = 'Sales';

departmentModel.getDepartmentByName(name, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Example 3: Get all departments
```
const departmentModel = require('./departmentModel');

const data = {
  searchDepartment: '',
  tablePage: 1,
  tableDisplayLength: 10,
  allTypes: true
};

departmentModel.getDepartments(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Example 4: Insert a new department
```
const departmentModel = require('./departmentModel');

const data = {
  name: 'Marketing'
};

departmentModel.insertDepartment(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Example 5: Update a department
```
const departmentModel = require('./departmentModel');

const data = {
  name: 'HR',
  id: 1
};

departmentModel.updateDepartment(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Example 6: Delete a department
```
const departmentModel = require('./departmentModel');

const id = 1;

departmentModel.deleteDepartment(id, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Methods:

1. getDepartmentsLength(callback)
   - Description: Retrieves the number of departments in the database.
   - Parameters:
     - callback: A function to be called with the result or error.
       - Parameters:
         - error: An object containing the error code and message.
         - result: The number of departments.
   - Returns: None.

2. getDepartmentByName(name, callback)
   - Description: Retrieves a department by its name.
   - Parameters:
     - name: The name of the department to retrieve.
     - callback: A function to be called with the result or error.
       - Parameters:
         - error: An object containing the error code and message.
         - result: The department record.
   - Returns: None.

3. getDepartments(data, callback)
   - Description: Retrieves a list of departments based on the provided data.
   - Parameters:
     - data: An object containing the search criteria and pagination information.
       - searchDepartment: The search term for filtering departments by name.
       - tablePage: The current page number.
       - tableDisplayLength: The number of departments to display per page.
       - allTypes: A boolean indicating whether to retrieve all types of departments.
     - callback: A function to be called with the result or error.
       - Parameters:
         - error: An object containing the error code and message.
         - result: The list of departments.
   - Returns: None.

4. insertDepartment(data, callback)
   - Description: Inserts a new department into the database.
   - Parameters:
     - data: An object containing the department details.
       - name: The name of the department.
     - callback: A function to be called with the result or error.
       - Parameters:
         - error: An object containing the error code and message.
         - result: The ID of the inserted department.
   - Returns: None.

5. updateDepartment(data, callback)
   - Description: Updates an existing department in the database.
   - Parameters:
     - data: An object containing the department details.
       - name: The new name of the department.
       - id: The ID of the department to update.
     - callback: A function to be called with the result or error.
       - Parameters:
         - error: An object containing the error code and message.
         - result: The number of affected rows.
   - Returns: None.

6. deleteDepartment(id, callback)
   - Description: Deletes a department from the database.
   - Parameters:
     - id: The ID of the department to delete.
     - callback: A function to be called with the result or error.
       - Parameters:
         - error: An object containing the error code and message.
         - result: The number of affected rows.
   - Returns: None.

Technical Concepts:

1. pool: The `pool` object is used to manage connections to the MySQL database. It is imported from the `mysqlPool` module.

2. getConnection: The `getConnection` method is used to get a connection from the connection pool. It takes a callback function as a parameter, which will be called with the connection object.

3. query: The `query` method is used to execute SQL queries on the database. It takes the SQL query string and an optional array of values as parameters. The callback function will be called with the error (if any) and the result of the query.

4. connection.release: The `release` method is used to release the connection back to the connection pool after executing a query.

5. status: The `status` column in the `department` table is used to indicate the status of a department. A status of 1 means the department is active, while a status of 0 means the department is inactive.

6. LIKE: The `LIKE` operator is used in SQL queries to perform pattern matching on string values. It is used in the `getDepartmentByName` and `getDepartments` methods to search for departments with names similar to the provided search term.

7. INSERT INTO: The `INSERT INTO` statement is used to insert new records into a database table. It is used in the `insertDepartment` method to add a new department to the `department` table.

8. UPDATE: The `UPDATE` statement is used to modify existing records in a database table. It is used in the `updateDepartment` and `deleteDepartment` methods to update the name and status of a department, respectively.

9. WHERE: The `WHERE` clause is used in SQL queries to specify a condition for filtering the result set. It is used in the `getDepartments` method to filter departments based on the search term and status.

10. module.exports: The `module.exports` statement is used to export the `companyModel` object, making it available for other modules to use.
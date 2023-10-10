# sentMailModel.js

## Description
This file contains the code for the sentMailModel, which is a model that manages the sent email record. It provides methods for adding a new sent email record and getting the number of emails sent in a specific day.

## Examples
Here are some examples of how to use the sentMailModel class:

```javascript
const sentMailModel = require('./sentMailModel');

// Example 1: Adding a new sent email record
const data = {
  type: 'confirmation'
};

sentMailModel.addRecord(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log('Sent email record added successfully');
  }
});

// Example 2: Getting the number of emails sent on a specific day
const date = new Date('2022-01-01');

sentMailModel.getSentEmailAmount(date, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(`Number of emails sent on ${date.toDateString()}: ${result.sent_emails}`);
  }
});
```

## Methods

### addRecord(data, callback)
Adds a new sent email record to the database.

#### Parameters
- `data` (object): An object containing all the information for the sent email record.
  - `type` (string): The type of the email as a string.
- `callback` (function): A callback function that will be called with the result or error.

### getSentEmailAmount(date, callback)
Gets the number of emails sent on a specific day.

#### Parameters
- `date` (Date): The date for which to get the number of sent emails.
- `callback` (function): A callback function that will be called with the result or error.

## Technical Concepts
- `pool`: The `pool` object is imported from the `mysqlPool` module and represents a pool of database connections. It is used to manage the connections to the database and handle the execution of SQL queries.
- `connection.query`: This method is used to execute an SQL query on a database connection. It takes the SQL query string as the first parameter and an optional array of values to replace placeholders in the query string. The result of the query is passed to the callback function.

## Dependencies
- `mysqlPool`: This module is required to establish a connection to the MySQL database and execute SQL queries.

## Export
The `sentEmailModel` object is exported as a module.
sentMailController.js

Description:
The sentMailController.js file is a JavaScript file that contains a function called getSentEmailAmmount. This function is responsible for retrieving the number of emails sent on a specific day. It interacts with the sentMailModel.js file to retrieve the data and handle any errors that may occur.

Examples:
Example 1:
```
GET /sent-emails?date=2021-10-01
```
This example retrieves the number of emails sent on October 1, 2021.

Example 2:
```
GET /sent-emails?date=2021-09-30
```
This example retrieves the number of emails sent on September 30, 2021.

Methods:
1. getSentEmailAmmount(request, response, next)
   - Description: This method retrieves the number of emails sent on a specific day.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - Returns: None.

Technical Concepts:
1. Date Validation:
   - The code checks if the provided date is valid by creating a new Date object from the given date string and checking if the resulting date string includes the word "Invalid". If it does, it means that the provided date is not valid.

File Content:

'use strict';

const sentMailModel = require('../models/sentMailModel');

/**
 * Gets the number of emails sent in a specific day
 */
function getSentEmailAmmount(request, response, next) {
  const { date } = request.query;
  if (!date) {
    return response.status(422).send({ error: 'Must provide date' });
  }

  const dateToCheck = new Date(date);
  if (dateToCheck.toString().includes('Invalid')) {
    return response.status(422).send({ error: 'Must provide a valid date' });
  }

  sentMailModel.getSentEmailAmmout(dateToCheck, (result, error) => {
    if (error) {
      return next({ ...error, params: request.params, body: request.body });
    }
  });
}

module.exports = { getSentEmailAmmount };
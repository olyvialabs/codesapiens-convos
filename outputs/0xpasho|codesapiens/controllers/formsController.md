formsController.js

Description:
This file contains the controller functions for handling forms-related actions. It includes functions for creating Excel files with form data.

createAnswersExcel(request, response, next) - This function creates an Excel file with the answers to a specific form. It takes in the request, response, and next parameters.

Parameters:
- request: The HTTP request object.
- response: The HTTP response object.
- next: The next middleware function.

Example usage:
createAnswersExcel(request, response, next);

createDeprecatedExcel(request, response, next) - This function creates an Excel file with deprecated form data. It takes in the request, response, and next parameters.

Parameters:
- request: The HTTP request object.
- response: The HTTP response object.
- next: The next middleware function.

Example usage:
createDeprecatedExcel(request, response, next);

createDataExcel(request, response, next) - This function creates an Excel file with form data. It takes in the request, response,
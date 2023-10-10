formTemplateModel.js

Description:
This file contains the code for the formTemplateModel class, which is responsible for interacting with the form_template table in the database. It provides methods for retrieving, inserting, updating, and deleting form templates.

Examples of how to use this class:

1. Get the length of the form templates:
   formTemplateModel.getFormTemplatesLength((error, result) => {
     if (error) {
       console.error(error);
     } else {
       console.log(result);
     }
   });

2. Get a list of form templates:
   const data = {
     searchTemplateEvaluation: 'example',
     tablePage: 1,
     tableDisplayLength: 10
   };
   formTemplateModel.getFormTemplates(data, (error, result) => {
     if (error) {
       console.error(error);
     } else {
       console.log(result);
     }
   });

3. Insert a new form template:
   const data = {
     name: 'New Template',
     description: 'This is a new form template'
   };
   formTemplateModel.insertFormTemplate(data, (error, result) => {
     if (error) {
       console.error(error);
     } else {
       console.log(result);
     }
   });

4. Update an existing form template:
   const data = {
     name: 'Updated Template',
     description: 'This is an updated form template',
     idform: 1
   };
   formTemplateModel.updateFormTemplate(data, (error, result) => {
     if (error) {
       console.error(error);
     } else {
       console.log(result);
     }
   });

5. Delete a form template:
   const data = {
     idform: 1
   };
   formTemplateModel.deleteFormTemplate(data, (error, result) => {
     if (error) {
       console.error(error);
     } else {
       console.log(result);
     }
   });

Methods:

1. getFormTemplatesLength(callback)
   - Description: Retrieves the length of the form templates.
   - Parameters:
     - callback: A function to be called with the result or error.
       - error: An object containing the error code and message.
       - result: The length of the form templates.
   - Returns: None.

2. getFormTemplates(data, callback)
   - Description: Retrieves a list of form templates based on the provided data.
   - Parameters:
     - data: An object containing the search criteria for the form templates.
       - searchTemplateEvaluation: A string to search for in the template name, description, and creation date.
       - tablePage: The current page number.
       - tableDisplayLength: The number of templates to display per page.
     - callback: A function to be called with the result or error.
       - error: An object containing the error code and message.
       - result: The list of form templates.
   - Returns: None.

3. insertFormTemplate(data, callback)
   - Description: Inserts a new form template into the database.
   - Parameters:
     - data: An object containing the name and description of the form template.
       - name: The name of the form template.
       - description: The description of the form template.
     - callback: A function to be called with the result or error.
       - error: An object containing the error code and message.
       - result: The result of the insertion operation.
   - Returns: None.

4. updateFormTemplate(data, callback)
   - Description: Updates an existing form template in the database.
   - Parameters:
     - data: An object containing the name, description, and ID of the form template.
       - name: The updated name of the form template.
       - description: The updated description of the form template.
       - idform: The ID of the form template to be updated.
     - callback: A function to be called with the result or error.
       - error: An object containing the error code and message.
       - result: The result of the update operation.
   - Returns: None.

5. deleteFormTemplate(data, callback)
   - Description: Deletes a form template from the database.
   - Parameters:
     - data: An object containing the ID of the form template to be deleted.
       - idform: The ID of the form template to be deleted.
     - callback: A function to be called with the result or error.
       - error: An object containing the error code and message.
       - result: The result of the delete operation.
   - Returns: None.

Technical Concepts:

1. pool: The pool object is used to manage connections to the MySQL database. It is imported from the mysqlPool module.

2. getConnection: The getConnection method is used to get a connection from the connection pool. It takes a callback function as a parameter, which is called with the connection object.

3. query: The query method is used to execute SQL queries on the database. It takes the query string and optional parameters as arguments, and a callback function to handle the result or error.

4. release: The release method is used to release the connection back to the connection pool after it is no longer needed.

5. JSON: JSON (JavaScript Object Notation) is a standard data interchange format that is easy for humans to read and write, and easy for machines to parse and generate. It is used to represent data in a structured way, similar to a dictionary or object in JavaScript.

Template Variables: None

Template File: N/A
formTemplateRoutes.js

Description:
The formTemplateRoutes.js file is a JavaScript module that defines the routes for handling form template-related requests in an Express.js application. It exports an Express Router object that can be used to define the routes for creating, retrieving, updating, and deleting form templates.

Code Explanation:
The code begins by importing the necessary dependencies. It requires the 'express' module and assigns it to the 'express' constant. It also imports the 'formTemplateController' module from the '../controllers/formTemplateController' path.

Next, it creates an instance of the Express Router using the 'express.Router()' method and assigns it to the 'api' constant.

The following routes are defined using the Router object:
1. POST '/': This route is used to insert a new form template. It calls the 'insertFormTemplate' method from the 'formTemplateController' module.
2. GET '/': This route is used to retrieve all form templates. It calls the 'getFormTemplate' method from the 'formTemplateController' module.
3. PUT '/:id': This route is used to update a specific form template identified by its 'id' parameter. It calls the 'updateFormTemplate' method from the 'formTemplateController' module.
4. DELETE '/:id': This route is used to delete a specific form template identified by its 'id' parameter. It calls the 'deleteFormTemplate' method from the 'formTemplateController' module.

Finally, the module exports the 'api' Router object, making it available for use in other parts of the application.

Examples of Usage:
Here are some examples of how to use the formTemplateRoutes.js module:

Example 1: Insert a new form template
```
POST /formTemplates
Request Body:
{
  "name": "Contact Form",
  "fields": [
    {
      "name": "Name",
      "type": "text"
    },
    {
      "name": "Email",
      "type": "email"
    }
  ]
}
```

Example 2: Retrieve all form templates
```
GET /formTemplates
```

Example 3: Update a form template
```
PUT /formTemplates/123
Request Body:
{
  "name": "Updated Form",
  "fields": [
    {
      "name": "Name",
      "type": "text"
    },
    {
      "name": "Email",
      "type": "email"
    },
    {
      "name": "Phone",
      "type": "tel"
    }
  ]
}
```

Example 4: Delete a form template
```
DELETE /formTemplates/123
```

Methods:

1. insertFormTemplate:
   - Description: Inserts a new form template into the database.
   - Parameters: None
   - Returns: Promise representing the newly inserted form template.

2. getFormTemplate:
   - Description: Retrieves all form templates from the database.
   - Parameters: None
   - Returns: Promise representing an array of form templates.

3. updateFormTemplate:
   - Description: Updates a specific form template identified by its 'id' parameter.
   - Parameters:
     - id (string): The unique identifier of the form template to be updated.
   - Returns: Promise representing the updated form template.

4. deleteFormTemplate:
   - Description: Deletes a specific form template identified by its 'id' parameter.
   - Parameters:
     - id (string): The unique identifier of the form template to be deleted.
   - Returns: Promise representing the deleted form template.

Technical Concepts:
- Express Router: The Express Router is a middleware that allows you to define routes for handling HTTP requests in an Express.js application. It provides methods for defining routes and associating them with specific request handlers.
- Promises: Promises are a way to handle asynchronous operations in JavaScript. They represent the eventual completion or failure of an asynchronous operation and allow you to chain multiple asynchronous operations together.

Template Variables: N/A

Template File: N/A
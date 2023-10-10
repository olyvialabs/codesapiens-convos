formActionRoutes.js

Description:
This file contains the routes for handling form actions in an application. It exports an Express router object that defines the various routes and their corresponding controller methods for performing CRUD operations on form actions. The routes are protected and require a valid token for authentication.

Code Explanation:
- The file begins with the import of necessary dependencies and modules.
- The 'express' module is required and used to create an instance of the Express router.
- The 'formActionController' module is required, which contains the controller methods for handling form actions.
- The 'verifyToken' function is imported from the 'verifyToken' module, which is a helper function used for token authentication.

Routes:
1. GET /:idform
   - Description: Retrieves all form actions associated with a specific form.
   - Parameters:
     - idform: The ID of the form for which to retrieve the form actions.
   - Example:
     - Request: GET /123
     - Response: Returns an array of form actions associated with the form ID 123.

2. POST /
   - Description: Adds a new form action.
   - Parameters: None
   - Example:
     - Request: POST /
       Body: { "name": "Submit", "action": "submitForm" }
     - Response: Returns the newly created form action object.

3. PUT /:idaction
   - Description: Updates an existing form action.
   - Parameters:
     - idaction: The ID of the form action to be updated.
   - Example:
     - Request: PUT /456
       Body: { "name": "Save", "action": "saveForm" }
     - Response: Returns the updated form action object.

4. DELETE /:idaction
   - Description: Deletes a form action.
   - Parameters:
     - idaction: The ID of the form action to be deleted.
   - Example:
     - Request: DELETE /789
     - Response: Returns a success message indicating the form action has been deleted.

Technical Concepts:
- Express Router: The Express router is a middleware that allows us to define routes and their corresponding handlers in separate modules and then use them in our main application.
- Token Authentication: The 'verifyToken' function is a helper function that verifies the authenticity of a token sent in the request header. It ensures that the user is authenticated before allowing access to the protected routes.

Template Variables: N/A

Template File: N/A
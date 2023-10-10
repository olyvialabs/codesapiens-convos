projectRoutes.js

Description:
The projectRoutes.js file is a JavaScript file that defines the routes for the project-related API endpoints in an Express application. It imports the projectController module and uses its methods to handle the corresponding HTTP requests. This file exports an Express Router instance that can be used in the main application file to mount these routes.

Code Explanation:
The code in projectRoutes.js sets up the routes for the project-related API endpoints. It uses the Express Router to define the routes and associates each route with a specific method from the projectController module.

Examples of Usage:
1. To insert a new project:
   - HTTP Method: POST
   - Endpoint: /
   - Request Body: JSON object representing the project details
   - Example:
     ```
     POST / HTTP/1.1
     Content-Type: application/json

     {
       "name": "Project 1",
       "description": "This is the first project"
     }
     ```

2. To get a project by ID:
   - HTTP Method: GET
   - Endpoint: /:id
   - Path Parameter: ID of the project
   - Example:
     ```
     GET /123 HTTP/1.1
     ```

3. To update a project by ID:
   - HTTP Method: PUT
   - Endpoint: /:id
   - Path Parameter: ID of the project
   - Request Body: JSON object representing the updated project details
   - Example:
     ```
     PUT /123 HTTP/1.1
     Content-Type: application/json

     {
       "name": "Updated Project 1",
       "description": "This is the updated project"
     }
     ```

4. To delete a project by ID:
   - HTTP Method: DELETE
   - Endpoint: /:id
   - Path Parameter: ID of the project
   - Example:
     ```
     DELETE /123 HTTP/1.1
     ```

Methods:

1. insertProject:
   - Description: Handles the HTTP POST request to insert a new project.
   - Parameters: None
   - Returns: None

2. getProject:
   - Description: Handles the HTTP GET request to retrieve a project by ID.
   - Parameters:
     - id (optional): The ID of the project to retrieve.
   - Returns: None

3. updateProject:
   - Description: Handles the HTTP PUT request to update a project by ID.
   - Parameters:
     - id: The ID of the project to update.
   - Returns: None

4. deleteProject:
   - Description: Handles the HTTP DELETE request to delete a project by ID.
   - Parameters:
     - id: The ID of the project to delete.
   - Returns: None

Technical Concepts:
- Express Router: The Express Router is a middleware that allows us to define multiple routes for our application. It helps in organizing the code and handling different HTTP methods for different endpoints.

- require: The require function is a built-in Node.js function used to import modules. In this file, it is used to import the projectController module, which contains the methods to handle the project-related API requests.

- module.exports: The module.exports object is a special object in Node.js that is used to export variables, functions, or objects from a module. In this file, it exports the Express Router instance, which can be used in other files to mount the defined routes.

Template Variables: N/A

Template File: N/A
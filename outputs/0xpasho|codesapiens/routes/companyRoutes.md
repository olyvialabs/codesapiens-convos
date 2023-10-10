companyRoutes.js

Description:
The companyRoutes.js file is a module that handles the routing for company-related requests in an Express.js application. It exports an instance of the Express Router with various routes and corresponding controller methods for creating, retrieving, updating, and deleting company data. Additionally, there are commented out sections related to handling company avatars.

Code Example:
```
'use strict'

const express = require('express');
//const multer = require('multer');
const api = express.Router();
const companyController = require('../controllers/companyController');
// Helpers
const { verifyToken } = require('../helpers/verifyToken');

// Create multer instance
/*const upload  = multer({
  dest: `${__dirname}/../images/temp/`
});*/

api.post('/', verifyToken, companyController.insertCompany);
api.get('/:id?', verifyToken, companyController.getCompany);
api.put('/:id', verifyToken, companyController.updateCompany);
api.delete('/:id', verifyToken, companyController.deleteCompany);

/* Company avatar routes */

// Upload/set avatar
//api.post('/avatar/:idcompany', verifyToken, upload.single('avatar'), companyController.setCompanyImage);
// Get avatar
//api.get('/avatar/:idcompany', companyController.getCompanyImage);

module.exports = api;
```

Methods:
1. `api.post('/')`
   - Description: This method handles the creation of a new company.
   - Parameters: None
   - Example:
     ```
     POST / HTTP/1.1
     Content-Type: application/json
     Authorization: Bearer <token>

     {
       "name": "Example Company",
       "address": "123 Example Street",
       "phone": "123-456-7890"
     }
     ```

2. `api.get('/:id?')`
   - Description: This method retrieves company data based on the provided ID. If no ID is provided, it returns all companies.
   - Parameters:
     - `id` (optional): The ID of the company to retrieve.
   - Example:
     ```
     GET /123 HTTP/1.1
     Authorization: Bearer <token>
     ```

3. `api.put('/:id')`
   - Description: This method updates an existing company based on the provided ID.
   - Parameters:
     - `id`: The ID of the company to update.
   - Example:
     ```
     PUT /123 HTTP/1.1
     Content-Type: application/json
     Authorization: Bearer <token>

     {
       "name": "Updated Company",
       "address": "456 Updated Street",
       "phone": "987-654-3210"
     }
     ```

4. `api.delete('/:id')`
   - Description: This method deletes an existing company based on the provided ID.
   - Parameters:
     - `id`: The ID of the company to delete.
   - Example:
     ```
     DELETE /123 HTTP/1.1
     Authorization: Bearer <token>
     ```

Technical Concepts:
- Express Router: The `express.Router()` function creates a new router object in Express.js. It allows for modularizing routes and middleware, making it easier to organize and maintain code.
- verifyToken: This is a helper function imported from the `verifyToken` module. It is used as middleware to verify the authenticity of a token before allowing access to protected routes.

Company Avatar Routes:
- The commented out sections in the code suggest the presence of routes related to handling company avatars. However, these routes are not currently active and are not part of the exposed API.

Template Variables: N/A (This is not a template file)

Overall, the companyRoutes.js file provides a set of routes for creating, retrieving, updating, and deleting company data in an Express.js application. It also includes commented out sections related to handling company avatars, which can be enabled and implemented as needed.
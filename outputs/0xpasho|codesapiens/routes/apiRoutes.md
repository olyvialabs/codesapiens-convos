apiRoutes.js

Description:
This file contains the API routes for the application. It imports various route files and controllers to handle different endpoints. It also includes a helper function for token verification. Additionally, it defines several API routes for handling visitors and uploading company avatars.

Code Explanation:
- The file starts by importing the necessary modules and route files using the `require` function.
- It also imports the `verifyToken` helper function from the `verifyToken.js` file.
- The `api` variable is initialized as an instance of the Express Router.
- The imported route files are then mounted on the `api` router using the `use` method.
- The `verifyToken` middleware is applied to the following routes: `/visitors/:id`, `/visitors-bulk/:idform`.
- The `formsController` is used to handle the following routes: `/visitors/:id`, `/visitors-bulk/:idform`.
- The `companyController` is used to handle the `/avatar/:idcompany` route.
- A `multer` instance is created to handle file uploads, with the destination set to the `../images/temp/` directory.
- The `/avatar/:idcompany` route is defined to handle file uploads and calls the `setCompanyImage` method from the `companyController`.
- Finally, the `api` router is exported as a module.

Examples of Usage:
1. Mounting the `companyRoutes` on the `/company` route:
   ```
   api.use('/company', companyRoutes);
   ```

2. Mounting the `projectRoutes` on the `/project` route:
   ```
   api.use('/project', projectRoutes);
   ```

3. Verifying token and updating a visitor using the `updateVisitor` method from `formsController`:
   ```
   api.put('/visitors/:id', verifyToken, formsController.updateVisitor);
   ```

4. Verifying token and inserting a visitor using the `insertVisitor` method from `formsController`:
   ```
   api.post('/visitors/:id', verifyToken, formsController.insertVisitor);
   ```

5. Verifying token and getting a visitor using the `getVisitor` method from `formsController`:
   ```
   api.get('/visitors/:id', verifyToken, formsController.getVisitor);
   ```

6. Verifying token and deleting a visitor using the `deleteVisitor` method from `formsController`:
   ```
   api.delete('/visitors/:id', verifyToken, formsController.deleteVisitor);
   ```

7. Verifying token and sending bulk emails to visitors using the `bulkEmailSend` method from `formsController`:
   ```
   api.get('/visitors-bulk/:idform', verifyToken, formsController.bulkEmailSend);
   ```

Methods:
1. `updateVisitor`:
   - Description: Updates a visitor's information.
   - Parameters:
     - `id` (string): The ID of the visitor to be updated.
   - Example:
     ```
     api.put('/visitors/:id', verifyToken, formsController.updateVisitor);
     ```

2. `insertVisitor`:
   - Description: Inserts a new visitor.
   - Parameters:
     - `id` (string): The ID of the visitor to be inserted.
   - Example:
     ```
     api.post('/visitors/:id', verifyToken, formsController.insertVisitor);
     ```

3. `getVisitor`:
   - Description: Retrieves a visitor's information.
   - Parameters:
     - `id` (string): The ID of the visitor to be retrieved.
   - Example:
     ```
     api.get('/visitors/:id', verifyToken, formsController.getVisitor);
     ```

4. `deleteVisitor`:
   - Description: Deletes a visitor.
   - Parameters:
     - `id` (string): The ID of the visitor to be deleted.
   - Example:
     ```
     api.delete('/visitors/:id', verifyToken, formsController.deleteVisitor);
     ```

5. `bulkEmailSend`:
   - Description: Sends bulk emails to visitors.
   - Parameters:
     - `idform` (string): The ID of the form for which bulk emails will be sent.
   - Example:
     ```
     api.get('/visitors-bulk/:idform', verifyToken, formsController.bulkEmailSend);
     ```

Technical Concepts:
- `multer`: Multer is a middleware for handling multipart/form-data, which is primarily used for file uploads. It is used in this file to handle file uploads and store the uploaded files in the specified destination directory.

Variables Used:
- `express`: The Express module.
- `api`: An instance of the Express Router.
- `multer`: The Multer module.
- `companyRoutes`: The imported company routes.
- `projectRoutes`: The imported project routes.
- `authRoutes`: The imported authentication routes.
- `formsRoutes`: The imported form routes.
- `notificationRoutes`: The imported notification routes.
- `formsController`: The imported forms controller.
- `companyController`: The imported company controller.
- `departmentRoutes`: The imported department routes.
- `templatesRoutes`: The imported template routes.
- `moduleRoutes`: The imported module routes.
- `sectionsRoutes`: The imported section routes.
- `formTemplateRoutes`: The imported form template routes.
- `formActionRoutes`: The imported form action routes.
- `similarOpinionRoutes`: The imported similar opinion routes.
- `verifyToken`: The imported token verification helper function.

Template File: N/A
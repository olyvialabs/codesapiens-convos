formsRoutes.js

Description:
This file contains the routes for handling form-related requests in the application. It exports an Express Router object that defines various routes and their corresponding controller methods. These routes are responsible for creating, editing, deleting, and retrieving form data.

Code Example:
```
'use strict';

const express = require('express');
const api = express.Router();
const formsController = require('../controllers/formsController');
// Helpers
const { verifyToken } = require('../helpers/verifyToken');

api.get('/generate/pdf/:idform', formsController.createPDF);
api.get('/generate/excel-data/:idform', formsController.createDataExcel);
api.get('/generate/excel-answers/:idform', formsController.createAnswersExcel);
api.post('/new', verifyToken, formsController.insertForm);
api.post('/edit/:id', verifyToken, formsController.editFormStructure);
api.post('/copy/:id', verifyToken, formsController.copyForm);
api.get('/info/:id?', verifyToken, formsController.getForm);
api.get('/editor/:id/:isTemplate?', verifyToken, formsController.getEditorForm);
api.post('/resolve/:id', verifyToken, formsController.resolveForm);
api.put('/:id', verifyToken, formsController.updateForm);
api.delete('/:id', verifyToken, formsController.deleteForm);
api.get('/verify/done/', verifyToken, formsController.haveAnyFormPending);
api.get('/tries/:idform', verifyToken, formsController.getFormTries);
api.get('/answers', verifyToken, formsController.getAnswersCount);
api.get('/questions/length/:id', verifyToken, formsController.getQuestionsLength);
module.exports = api;
```

Methods:
1. createPDF
   - Description: Generates a PDF file for a specific form.
   - Example: GET /generate/pdf/:idform
   - Parameters:
     - idform (string): The ID of the form for which the PDF is to be generated.

2. createDataExcel
   - Description: Generates an Excel file containing the form data.
   - Example: GET /generate/excel-data/:idform
   - Parameters:
     - idform (string): The ID of the form for which the Excel file is to be generated.

3. createAnswersExcel
   - Description: Generates an Excel file containing the form answers.
   - Example: GET /generate/excel-answers/:idform
   - Parameters:
     - idform (string): The ID of the form for which the Excel file is to be generated.

4. insertForm
   - Description: Inserts a new form into the database.
   - Example: POST /new
   - Parameters: None

5. editFormStructure
   - Description: Edits the structure of a form.
   - Example: POST /edit/:id
   - Parameters:
     - id (string): The ID of the form to be edited.

6. copyForm
   - Description: Creates a copy of a form.
   - Example: POST /copy/:id
   - Parameters:
     - id (string): The ID of the form to be copied.

7. getForm
   - Description: Retrieves information about a specific form.
   - Example: GET /info/:id?
   - Parameters:
     - id (string, optional): The ID of the form to be retrieved. If not provided, retrieves all forms.

8. getEditorForm
   - Description: Retrieves a form for editing in the form editor.
   - Example: GET /editor/:id/:isTemplate?
   - Parameters:
     - id (string): The ID of the form to be retrieved.
     - isTemplate (boolean, optional): Specifies whether the form is a template. Default is false.

9. resolveForm
   - Description: Resolves a form, marking it as completed.
   - Example: POST /resolve/:id
   - Parameters:
     - id (string): The ID of the form to be resolved.

10. updateForm
    - Description: Updates the details of a form.
    - Example: PUT /:id
    - Parameters:
      - id (string): The ID of the form to be updated.

11. deleteForm
    - Description: Deletes a form from the database.
    - Example: DELETE /:id
    - Parameters:
      - id (string): The ID of the form to be deleted.

12. haveAnyFormPending
    - Description: Checks if there are any forms pending verification.
    - Example: GET /verify/done/
    - Parameters: None

13. getFormTries
    - Description: Retrieves the number of tries for a specific form.
    - Example: GET /tries/:idform
    - Parameters:
      - idform (string): The ID of the form to retrieve the number of tries for.

14. getAnswersCount
    - Description: Retrieves the count of form answers.
    - Example: GET /answers
    - Parameters: None

15. getQuestionsLength
    - Description: Retrieves the length of questions in a specific form.
    - Example: GET /questions/length/:id
    - Parameters:
      - id (string): The ID of the form to retrieve the length of questions for.

Technical Concepts:
- Express Router: The `express.Router()` function creates a new router object in Express. It allows us to define routes and their corresponding handler functions.
- verifyToken: This is a helper function imported from the `verifyToken` module. It is used as middleware to verify the authenticity of a user's token before allowing access to certain routes.

Note: The file also imports the `formsController` module, which contains the implementation of the controller methods for handling form-related operations. However, the details of these methods are not provided in this file.
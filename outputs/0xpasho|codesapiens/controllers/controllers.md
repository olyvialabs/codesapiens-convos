# controllers

This folder contains various controller files that are responsible for handling different functionalities in the system. Each controller file exports functions that can be used in the corresponding routes of an Express application. These functions interact with the respective model modules to perform database operations and handle specific actions.

## Files

### [authController.md](controllers/authController.md)

This file contains the controller functions for handling user authentication and user management. It exports several functions that can be used in the authentication routes of an Express application. The functions interact with the authModel module to perform database operations related to user authentication and management.

### [moduleController.md](controllers/moduleController.md)

This file contains the controller functions for handling modules. It exports functions that are used to retrieve, insert, update, and delete modules from the database. The controller functions interact with the moduleModel module to perform database operations related to modules.

### [departmentController.md](controllers/departmentController.md)

This file contains the controller functions for handling departments. It exports functions that are used to retrieve, insert, update, and delete departments from the database. The controller functions interact with the departmentModel module to perform database operations related to departments.

### [sectionController.md](controllers/sectionController.md)

This file contains the controller functions for handling sections. It exports functions that are used to retrieve, insert, update, and delete sections from the database. The controller functions interact with the sectionModel module to perform database operations related to sections.

### [formsController.md](controllers/formsController.md)

This file contains the controller functions for handling forms-related actions. It includes functions for creating Excel files with form data. The controller functions interact with the formsModel module to perform database operations related to forms.

### [formActionController.md](controllers/formActionController.md)

This file contains the controller functions for handling form actions. It exports functions that are used to perform actions on forms, such as submitting, updating, and deleting forms. The controller functions interact with the formActionModel module to perform database operations related to form actions.

### [formTemplateController.md](controllers/formTemplateController.md)

This file contains the controller functions for handling form templates. It exports functions that are used to retrieve, insert, update, and delete form templates from the database. The controller functions interact with the formTemplateModel module to perform database operations related to form templates.

### [sentMailController.md](controllers/sentMailController.md)

This file contains the controller functions for handling sent emails. It includes a function for retrieving the number of emails sent on a specific day. The controller function interacts with the sentMailModel module to retrieve the data and handle any errors that may occur.

### [templatesController.md](controllers/templatesController.md)

This file contains the controller functions for handling requests related to templates. It utilizes the templatesModel module to interact with the database and perform CRUD operations on templates. The controller functions handle various HTTP methods such as GET, POST, PUT, and DELETE to retrieve, create, update, and delete templates.

### [notificationController.md](controllers/notificationController.md)

This file contains the implementation of a notification controller. It includes functions for adding a notification record to the database, retrieving visitor notifications, retrieving unanswered forms, sending reminder/access emails, and resending emails. The controller interacts with the notificationModel module to perform database operations related to notifications.

### [companyController.md](controllers/companyController.md)

This file contains the controller functions for handling companies. It exports functions that are used to retrieve, insert, update, and delete companies from the database. The controller functions interact with the companyModel module to perform database operations related to companies.

### [projectController.md](controllers/projectController.md)

This file contains the controller functions for handling projects. It exports functions that are used to retrieve, insert, update, and delete projects from the database. The controller functions interact with the projectModel module to perform database operations related to projects.

### [similarOpinionController.md](controllers/similarOpinionController.md)

This file contains functions for handling similar opinions and strategies related to a specific section. It exports functions that are used to add similar opinions, retrieve similar opinions, and perform other related actions. The controller functions interact with the similarOpinionModel module to perform database operations related to similar opinions and strategies.
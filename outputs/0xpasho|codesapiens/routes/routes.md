# routes

The "routes" folder contains various files that define the routes for handling different operations in the system. These routes are responsible for handling HTTP requests and mapping them to the corresponding controller methods. Each file in this folder focuses on a specific aspect of the system and defines the routes related to that aspect.

## [formTemplateRoutes.md](routes/formTemplateRoutes.md)

The formTemplateRoutes.js file is a JavaScript module that defines the routes for handling form template-related requests in an Express.js application. It exports an Express Router object that can be used to define the routes for creating, retrieving, updating, and deleting form templates.

## [formsRoutes.md](routes/formsRoutes.md)

This file contains the routes for handling form-related requests in the application. It exports an Express Router object that defines various routes and their corresponding controller methods. These routes are responsible for creating, editing, deleting, and retrieving form data.

## [moduleRoutes.md](routes/moduleRoutes.md)

The moduleRoutes.js file is a JavaScript file that defines the routes for the module-related operations in an application. It uses the Express framework to create a router object and defines various HTTP methods (GET, POST, PUT, DELETE) for different module operations. These routes are associated with corresponding controller methods.

## [formActionRoutes.md](routes/formActionRoutes.md)

This file contains the routes for handling form actions in an application. It exports an Express router object that defines the various routes and their corresponding controller methods for performing CRUD operations on form actions. The routes are protected and require a valid token for authentication.

## [apiRoutes.md](routes/apiRoutes.md)

This file contains the API routes for the application. It imports various route files and controllers to handle different endpoints. It also includes a helper function for token verification. Additionally, it defines several API routes for handling visitors and uploading company avatars.

## [companyRoutes.md](routes/companyRoutes.md)

The companyRoutes.js file is a module that handles the routing for company-related requests in an Express.js application. It exports an instance of the Express Router with various routes and corresponding controller methods for creating, retrieving, updating, and deleting company data. Additionally, there are commented-out routes for handling company invitations.

## [sectionRoutes.md](routes/sectionRoutes.md)

The sectionRoutes.js file is a module that handles the routing for section-related operations in an application. It exports an Express router object that contains various routes for handling HTTP requests related to sections. These routes are associated with corresponding methods in the sectionController.js file.

## [templatesRoutes.md](routes/templatesRoutes.md)

This file is a JavaScript module that defines the routes for templates in an Express application. It exports an Express Router object that handles HTTP requests for creating, retrieving, updating, and deleting templates. The routes are mapped to corresponding methods in the templatesController module.

## [departmentRoutes.md](routes/departmentRoutes.md)

The departmentRoutes.js file is a module that handles the routing for department-related API endpoints in a web application. It uses the Express.js framework to define the routes and map them to corresponding controller functions. The file exports an Express Router instance that can be used in the main application.

## [similarOpinionRoutes.md](routes/similarOpinionRoutes.md)

This file contains the routes for handling similar opinions and strategies related to a specific section. It uses the Express framework for routing and the similarOpinionController for handling the logic of each route. The routes are protected and require a valid token for authentication.

## [notificationRoutes.md](routes/notificationRoutes.md)

This file contains the routes for handling notifications in an application. It exports an Express Router object that can be used to define the routes for handling various notification-related operations. The routes are associated with corresponding methods from the notificationController module.

## [authRoutes.md](routes/authRoutes.md)

This file contains the routes for authentication in the application. It includes various endpoints for user authentication, such as signing up, signing in, changing password, restoring password, and managing user accounts. The routes are implemented using the Express.js framework and are handled by the authController module.

## [projectRoutes.md](routes/projectRoutes.md)

The projectRoutes.js file is a JavaScript file that defines the routes for the project-related API endpoints in an Express application. It imports the projectController module and uses its methods to handle the corresponding HTTP requests. This file exports an Express Router instance that can be used in the main application.
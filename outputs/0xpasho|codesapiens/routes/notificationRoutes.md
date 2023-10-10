notificationRoutes.js

Description:
This file contains the routes for handling notifications in an application. It exports an Express Router object that can be used to define the routes for handling various notification-related operations. The routes are associated with corresponding methods from the notificationController module.

Code Explanation:
The code begins by importing the necessary modules and dependencies. The 'express' module is required to create an instance of the Express Router. The 'notificationController' module is required to access the methods for handling notification-related operations. The 'verifyToken' helper function is imported from the 'verifyToken' module to authenticate and authorize the requests.

The code then defines the routes using the Express Router object. Each route is associated with a specific HTTP method and a corresponding method from the 'notificationController' module. The routes are as follows:

1. GET /pending_forms:
   - This route is used to retrieve a list of pending forms that have not been answered.
   - It requires the user to be authenticated and authorized, which is done by calling the 'verifyToken' function as a middleware.
   - The corresponding method in the 'notificationController' module that handles this route is 'getNoAnsweredForms'.

2. GET /resendFormz:
   - This route is used to resend emails for forms that have not been answered.
   - It does not require authentication or authorization.
   - The corresponding method in the 'notificationController' module that handles this route is 'resendEmails'.

3. POST /visitor:
   - This route is used to retrieve notifications for a specific visitor.
   - It requires the user to be authenticated and authorized.
   - The corresponding method in the 'notificationController' module that handles this route is 'getVisitorNotifications'.

4. POST /add:
   - This route is used to add a new notification record.
   - It requires the user to be authenticated and authorized.
   - The corresponding method in the 'notificationController' module that handles this route is 'addNotificationRecord'.

5. POST /send_email/:type:
   - This route is used to send an email notification of a specific type.
   - It requires the user to be authenticated and authorized.
   - The corresponding method in the 'notificationController' module that handles this route is 'sendEmail'.

Finally, the code exports the Express Router object as 'api', making it available for use in other modules.

Examples of Usage:
Example 1: Retrieving pending forms
GET /pending_forms

Example 2: Resending emails for unanswered forms
GET /resendFormz

Example 3: Retrieving visitor notifications
POST /visitor
Request body:
{
  "visitorId": "1234567890"
}

Example 4: Adding a new notification record
POST /add
Request body:
{
  "title": "New Notification",
  "message": "This is a new notification."
}

Example 5: Sending an email notification
POST /send_email/welcome
Request body:
{
  "email": "example@example.com"
}

Technical Concepts:
- Express Router: The Express Router is a middleware that allows you to define routes for handling HTTP requests in an Express application. It provides a way to modularize and organize the routes in separate files.
- Middleware: Middleware functions are functions that have access to the request and response objects, and the next middleware function in the application's request-response cycle. They can be used to perform tasks such as authentication, logging, and error handling.
- Authentication: Authentication is the process of verifying the identity of a user or system. In this file, the 'verifyToken' function is used as a middleware to authenticate and authorize the requests by checking the validity of the token provided in the request headers.

Variables Used:
- express: The express module is used to create an instance of the Express Router.
- api: The Express Router object that will be used to define the notification routes.
- notificationController: The module that contains the methods for handling notification-related operations.
- verifyToken: The helper function for verifying the authentication token.

Template File:
N/A
notificationController.js

Description:
This file contains the implementation of a notification controller. It includes functions for adding a notification record to the database, retrieving visitor notifications, retrieving unanswered forms, sending reminder/access emails, and resending emails. The controller interacts with the notificationModel and authModel to perform database operations and with the sendNotificationEmail and generateRandomPassword helper functions for sending emails and generating random passwords, respectively.

Examples of how to use this class:

1. Adding a notification record:
   - Request:
     ```
     POST /notification
     {
       "iduser": 123,
       "idform": 456
     }
     ```
   - Response:
     ```
     {
       "message": "Notification added successfully"
     }
     ```

2. Retrieving visitor notifications:
   - Request:
     ```
     GET /notification/visitor
     {
       "iduser": 123
     }
     ```
   - Response:
     ```
     [
       {
         "id": 1,
         "message": "You have a new notification"
       },
       {
         "id": 2,
         "message": "Another notification"
       }
     ]
     ```

3. Retrieving unanswered forms:
   - Request:
     ```
     GET /notification/unanswered
     ```
   - Response:
     ```
     [
       {
         "id": 1,
         "form_name": "Form 1"
       },
       {
         "id": 2,
         "form_name": "Form 2"
       }
     ]
     ```

4. Sending a reminder/access email:
   - Request:
     ```
     POST /notification/email/reminder
     {
       "iduser": 123,
       "idform": 456
     }
     ```
   - Response:
     ```
     {
       "message": "Email sent successfully"
     }
     ```

5. Resending emails:
   - Request:
     ```
     POST /notification/email/resend
     ```
   - Response:
     ```
     {
       "message": "Emails resent successfully"
     }
     ```

Methods:

1. addNotificationRecord(request, response, next)
   - Description: Adds a notification record to the database.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - Returns: None.

2. getVisitorNotifications(request, response, next)
   - Description: Retrieves all visitor notifications.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - Returns: An array of visitor notifications.

3. getNoAnsweredForms(request, response, next)
   - Description: Retrieves unanswered forms.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - Returns: An array of unanswered forms.

4. sendEmail(request, response, next)
   - Description: Sends a reminder/access email.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - Returns: None.

5. resendEmails(request, response, next)
   - Description: Resends emails.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - Returns: None.

Technical Concepts:

1. JSON: JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. It is based on a subset of the JavaScript Programming Language, Standard ECMA-262 3rd Edition - December 1999. JSON is a text format that is completely language independent but uses conventions that are familiar to programmers of the C-family of languages, including C, C++, C#, Java, JavaScript, Perl, Python, and many others. These properties make JSON an ideal data-interchange language.

Variables used in the template file: N/A

Template file: N/A
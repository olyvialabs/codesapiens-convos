authController.js

Description:
This file contains the controller functions for handling user authentication and user management. It exports several functions that can be used in the authentication routes of an Express application. The functions interact with the authModel module to perform database operations related to user authentication and management.

Examples of how to use this class:
1. To create a new user:
   - Make a POST request to the '/signup' route with the following JSON body:
     {
       "name": "John Doe",
       "email": "johndoe@example.com",
       "password": "password123",
       "type": "user"
     }
   - The function will create a new user in the database with the provided information.

2. To authenticate a user:
   - Make a POST request to the '/signin' route with the following JSON body:
     {
       "email": "johndoe@example.com",
       "password": "password123"
     }
   - The function will verify the user's credentials and return a JWT token and user data if the credentials are correct.

3. To get all users:
   - Make a GET request to the '/users' route with optional query parameters:
     - page: The page number of the results (required)
     - pageLength: The number of users per page (required)
     - search: A search query to filter users (optional)
   - The function will retrieve all users from the database based on the provided parameters.

4. To update a user:
   - Make a PUT request to the '/users/:id' route with the following JSON body:
     {
       "name": "John Doe",
       "email": "johndoe@example.com",
       "type": "admin",
       "password": "newpassword123"
     }
   - The function will update the user's information in the database with the provided data.

5. To delete a user:
   - Make a DELETE request to the '/users/:id' route.
   - The function will delete the user from the database.

6. To change a user's password:
   - Make a POST request to the '/change-password' route with the following JSON body:
     {
       "newPassword": "newpassword123"
     }
   - The function will change the user's password to the new password provided.

7. To request a password change:
   - Make a POST request to the '/request-password-change' route with the following JSON body:
     {
       "email": "johndoe@example.com"
     }
   - The function will check if the user exists and send a restore link to the user's email if the user is found.

8. To check if a restore request exists:
   - Make a POST request to the '/check-restore-request' route with the following JSON body:
     {
       "idrestorepassword": "1234567890"
     }
   - The function will check if a restore request with the provided ID exists in the database.

9. To restore a password:
   - Make a POST request to the '/restore-password' route with the following JSON body:
     {
       "idrestorepassword": "1234567890",
       "iduser": "1",
       "newPassword": "newpassword123"
     }
   - The function will restore the user's password with the new password provided and mark the restore request as completed.

Methods:
1. signup(request, response, next)
   - Description: Creates a new user in the database.
   - Parameters:
     - request: JSON object that contains all the information from the `POST` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

2. signin(request, response, next)
   - Description: Looks for a user information and if correct returns a JWT token and user data.
   - Parameters:
     - request: JSON object that contains all the information from the `POST` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

3. getAllUsers(request, response, next)
   - Description: Get all users in the database.
   - Parameters:
     - request: JSON object that contains all the information from the `GET` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

4. updateUser(request, response, next)
   - Description: Updates user's data in the database.
   - Parameters:
     - request: JSON object that contains all the information from the `PUT` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

5. deleteUser(request, response, next)
   - Description: Deletes user from the database.
   - Parameters:
     - request: JSON object that contains all the information from the `DELETE` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

6. changePassword(request, response, next)
   - Description: Sends user information once the token sent was validated.
   - Parameters:
     - request: JSON object that contains all the information from the `POST` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

7. requestPasswordChange(request, response, next)
   - Description: Checks if user exist and sends a restore link.
   - Parameters:
     - request: JSON object that contains all the information from the `POST` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

8. checkRestoreRequest(request, response, next)
   - Description: Checks if exist a restore request.
   - Parameters:
     - request: JSON object that contains all the information from the `POST` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.

9. restorePassword(request, response, next)
   - Description: Restores password with the new one provided by the restore password form.
   - Parameters:
     - request: JSON object that contains all the information from the `POST` request.
     - response: Server response to the final user.
     - next: Express method that jumps into the next route function.
formTemplateController.js

Description:
This file contains the controller functions for handling form templates. It imports the formTemplateModel module and exports four functions: getFormTemplate, insertFormTemplate, updateFormTemplate, and deleteFormTemplate. These functions are used to retrieve, insert, update, and delete form templates from the database.

Examples of how to use this class:
1. To retrieve form templates:
   - Call the getFormTemplate function with the following parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - The function will retrieve form templates based on the provided query parameters (searchTemplateEvaluation, tablePage, tableDisplayLength) and send the response with the retrieved data.

2. To insert a form template:
   - Call the insertFormTemplate function with the following parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - The function will insert a new form template into the database based on the provided name and description in the request body. It will send the response with the ID of the inserted form template.

3. To update a form template:
   - Call the updateFormTemplate function with the following parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - The function will update an existing form template in the database based on the provided ID in the request parameters and the updated name and description in the request body. It will send the response with the updated data.

4. To delete a form template:
   - Call the deleteFormTemplate function with the following parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.
   - The function will delete a form template from the database based on the provided ID in the request parameters. It will send the response with a success message.

Methods:

1. getFormTemplate(request, response, next)
   - Description: Retrieves form templates from the database based on the provided query parameters.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.

2. insertFormTemplate(request, response, next)
   - Description: Inserts a new form template into the database.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.

3. updateFormTemplate(request, response, next)
   - Description: Updates an existing form template in the database.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.

4. deleteFormTemplate(request, response, next)
   - Description: Deletes a form template from the database.
   - Parameters:
     - request: The HTTP request object.
     - response: The HTTP response object.
     - next: The next middleware function.

Technical Concepts:
- None apparent in the code.

Code:

'use strict'

const path = require('path');
const fs = require('fs');

const formTemplateModel = require('../models/formTemplateModel');

function getFormTemplate(request, response, next) {
  const {searchTemplateEvaluation, tablePage, tableDisplayLength} = request.query;
  
  formTemplateModel.getFormTemplatesLength( (err, data) => {
    if(err) return next({...err, params: request.params, body: request.body});
    const formTemplatesLength = data[0].formtemplate_length;
    formTemplateModel.getFormTemplates({searchTemplateEvaluation, tablePage, tableDisplayLength}, 
      (err, data) => {
        if(err) 
          return next({...err, params: request.params, body: request.body});
        response.status(200).send({
          data: { rows: data, formTemplatesLength }
        });
      }
    );
  });
}

function insertFormTemplate(request, response, next) {
  const { name, description } = request.body;
  formTemplateModel.insertFormTemplate( {name, description}, (err, data) => {
    if(err) return next({...err, params: request.params, body: request.body});
    request.params.idform = data.insertId;
    response.status(200).send({
      data: { idform: data.insertId }
    });
  });
};

function updateFormTemplate(request, response, next) {
  const { id } = request.params;
  const { name, description } = request.body;
  formTemplateModel.updateFormTemplate( {name, description, idform: id}, 
    (err, data) => {
      if(err) return next({...err, params: request.params, body: request.body});
      response.status(200).send({data});
    }
  );
}

function deleteFormTemplate(request, response, next) {
  const { id } = request.params; 
  formTemplateModel.deleteFormTemplate( {idform: id}, (err, data) => {
    if(err) return next({...err, params: request.params, body: request.body});
    response.status(200).send({data: 'OK'});
  });
}

module.exports = {
  getFormTemplate,
  insertFormTemplate,
  updateFormTemplate,
  deleteFormTemplate,
};
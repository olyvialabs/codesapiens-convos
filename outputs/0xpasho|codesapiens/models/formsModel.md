# formsModel.js

## Description
The `formsModel.js` file contains the code for interacting with the database and performing various operations related to forms. It provides methods for retrieving forms, inserting new forms, updating forms, and getting information about form questions and answers.

## Examples
Here are some examples of how to use the `formsModel` class:

1. Get the length of all forms:
```javascript
formsModel.getFormsLength((error, result) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

2. Get a list of forms with pagination and search filters:
```javascript
const data = {
  searchForm: 'example',
  tablePage: 1,
  tableDisplayLength: 10,
  idcompany: 1
};

formsModel.getForms(data, (error, result) => {
  if (error) {
    console.error(error);
  } else {
    console
similarOpinionModel.js

Description:
The "similarOpinionModel.js" file is a module that manages similar opinions for answered forms in a database. It provides functions to insert similar opinions, retrieve all similar opinions and not related opinions, delete similar opinions, and manage strategies for a section.

Examples of how to use this class:

1. Insert Similar Opinion:
```javascript
const similarOpinionModel = require('similarOpinionModel');

const data = {
  idsection: 1,
  idopinion: 'abc123'
};

similarOpinionModel.insertSimilarOpinion(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

2. Get All Section Opinions:
```javascript
const similarOpinionModel = require('similarOpinionModel');

const data = {
  idsection: 1
};

similarOpinionModel.getAllSectionOpinions(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

3. Delete Similar Opinion:
```javascript
const similarOpinionModel = require('similarOpinionModel');

const data = {
  idsection: 1,
  idopinion: 'abc123'
};

similarOpinionModel.deleteSimilarOpinion(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

4. Get All Strategies:
```javascript
const similarOpinionModel = require('similarOpinionModel');

const data = {
  idsection: 1
};

similarOpinionModel.getAllStrategies(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

5. Add Strategy:
```javascript
const similarOpinionModel = require('similarOpinionModel');

const data = {
  description: 'Sample strategy',
  idsection: 1,
  idform: 'xyz789'
};

similarOpinionModel.addStrategy(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

6. Delete Strategy:
```javascript
const similarOpinionModel = require('similarOpinionModel');

const data = {
  idstrategy: 1
};

similarOpinionModel.deleteStrategy(data, (result, error) => {
  if (error) {
    console.error(error);
  } else {
    console.log(result);
  }
});
```

Methods:

1. insertSimilarOpinion(data, callback)
   - Description: Adds the similar opinions for the answered forms in the database.
   - Parameters:
     - data (object): Contains the following information:
       - idsection (number): Section Form ID.
       - idopinion (string): Opinion for the Section that was resolved.
     - callback (function): A callback function to handle the result or error.
   - Returns: The result of the database operation or an error.

2. getAllSectionOpinions(data, callback)
   - Description: Gets all similar opinions and not related opinions added in the database for a specific section.
   - Parameters:
     - data (object): Contains the following information:
       - idsection (number): Section ID.
     - callback (function): A callback function to handle the result or error.
   - Returns: An array of objects representing the opinions, with an additional "isRelated" property indicating if the opinion is related to a similar opinion or not.

3. deleteSimilarOpinion(data, callback)
   - Description: Deletes a similar opinion from the database.
   - Parameters:
     - data (object): Contains the following information:
       - idsection (number): Section ID.
       - idopinion (number): ID from the form response opinion about the section.
     - callback (function): A callback function to handle the result or error.
   - Returns: The result of the database operation or an error.

4. getAllStrategies(data, callback)
   - Description: Gets all strategies for a section.
   - Parameters:
     - data (object): Contains the following information:
       - idsection (number): Section ID.
     - callback (function): A callback function to handle the result or error.
   - Returns: An array of objects representing the strategies.

5. addStrategy(data, callback)
   - Description: Adds a strategy to the database.
   - Parameters:
     - data (object): Contains the following information:
       - description (string): Description of the strategy.
       - idsection (number): Section ID.
       - idform (string): Form ID.
     - callback (function): A callback function to handle the result or error.
   - Returns: The result of the database operation or an error.

6. deleteStrategy(data, callback)
   - Description: Deletes a strategy from the database.
   - Parameters:
     - data (object): Contains the following information:
       - idstrategy (number): Strategy ID.
     - callback (function): A callback function to handle the result or error.
   - Returns: The result of the database operation or an error.
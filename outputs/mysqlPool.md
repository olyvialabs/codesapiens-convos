

# Function name: mysql 

Function: 
```
require('mysql')
```, 
Documentation: 

https://www.npmjs.com/package/mysql

MySQL is an open source relational database management system (RDBMS) based on Structured Query Language (SQL). It is one of the most popular databases in the world and is used in a wide variety of applications, ranging from small websites to large enterprise applications. MySQL is used to store, retrieve, and manage data in a relational database. It is also used to create and manage databases, tables, and other objects. MySQL is a popular choice for web applications, and is used by many popular websites and applications, including WordPress, Drupal, and Joomla.

# Function name: pool 

Function: 
```
mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: process.env.NODE_ENV === 'prod' ? 'Tacos_smar_mysql' : '',
    database: 'smartkaizen'
})
```, 
Documentation: 

https://www.npmjs.com/package/mysql#pooling-connections
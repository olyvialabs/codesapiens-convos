# lectorCantidad.py

## Description
The "lectorCantidad.py" file is a Python script that converts a given number into its corresponding word representation in Spanish. The script takes a numerical input from the user and converts it into words, following the Spanish language rules for number naming.

## Examples
Here are a few examples of how to use this script:

Example 1:
```
Cual numero quieres convertir a letra: 1234
Output: "mil doscientos treinta y cuatro"
```

Example 2:
```
Cual numero quieres convertir a letra: 56
Output: "cincuenta y seis"
```

Example 3:
```
Cual numero quieres convertir a letra: 1000
Output: "mil"
```

## Method Descriptions

### `convert_number_to_word()`
This method takes a numerical input and converts it into its corresponding word representation in Spanish. It follows the Spanish language rules for number naming.

#### Parameters
- `numero` (string): The numerical input to be converted into words.

#### Technical Concepts
None

## File Content Description
The "lectorCantidad.py" file contains a Python script that converts a given number into its corresponding word representation in Spanish. The script uses a series of conditional statements and string concatenation to build the word representation of the number.

The script first prompts the user to enter a number. It then initializes several variables to store the individual digits of the number (entero, decenas, cien, miles). The script also initializes a counter variable (contador) to keep track of the current digit being processed.

The script then checks the length of the input number to determine the number of digits it has. Based on the number of digits, the script enters different conditional blocks to assign the digits to the corresponding variables.

After assigning the digits, the script checks if the sum of all the digits is zero. If it is, the script prints "cero" (zero). Otherwise, it proceeds to build the word representation of the number.

The script uses a series of conditional statements to determine the word representation of each digit and assigns the corresponding word to the concatenar variables (concatenar1, concatenar2, concatenar3, concatenar4). The concatenar variables are then used to build the final word representation of the number.

Finally, the script prints the word representation of the number by concatenating the concatenar variables in the correct order.

Note: The script currently uses the "print" statement to display the word representation of the number. If you want to use this script as a module, you can modify it to return the word representation as a string instead of printing it.


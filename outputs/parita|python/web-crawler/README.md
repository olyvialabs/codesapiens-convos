## All file content
A WEB-SCRAPER

Description:
This is a python code that allows you to make a database with fields-company name, contact no. and address- for amy category valid on justdial.com.
The output is in the .xls file format(Excel format).
This code has been tested only for the site:"http://www.justdial.com".

What you need?
->You'll need to install python on you machines if you don't already have it. It can be found here: http://www.python.org/getit/
->Python modules you'll need:
	BeautifulSoup (can be found here: http://www.crummy.com/software/BeautifulSoup/#Download)
	xlutils (can be found here: http://pypi.python.org/pypi/xlutils#downloads)
	
How to make use of it?
First thing you need to do is pull/download the file "crawl.py" and save it in a folder.
Next open your terminal/command prompt and go to the directory where you saved you "crawl.py" file.
Run the command "python crawl.py" in your terminal.
Type in the city you want your search to be restricted in and the categpry when asked. Now sit back and relax.
Check the folder where you saved you code. You'll find your .xls file ready with all the database of contact details you need, saved by the name of your category.
No more tedious work of copy-pasting to make a database!

Here's sample test that i did.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

C:\Documents and Settings\Suresh\python\web-crawler>python crawl.py
City: mumbai
Category: elevator-manufacturers
http://www.justdial.com/Mumbai/Elevator-manufacturers
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-2
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-2
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-3
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-3
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-4
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-4
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-5
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-5
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-6
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-6
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-7
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-7
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-8
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-8
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-9
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-9
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-10
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-10
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-11
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-11
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-12
http://www.justdial.com/Mumbai/Elevator%20Manufacturers/ct-17744/page-12

C:\Documents and Settings\Suresh\python\web-crawler>

----------------------------------------------------------------------------------------------------------------------


Output file: elevator-manufacturers.xls



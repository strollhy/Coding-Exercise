Wellspring_Ex
=============
Data Web Server for Wellspring Exercise
(http://wellspring-ex.appspot.com/)

Instruction
=============
  This a data web server hosted on Google App Engine. 
  It is using SQL databse, and supports basic data operations including:
  
  1. Display all data (default, sort by run number).
  2. Upload new csv file.
  3. Create new data.
  4. Edit data.
  5. Delete data.
  

Manual
=============
1. Upload new csv file:
   Click 'Choose File' button, select the csv to submit, after selection click 'Upload'.
   Then the page will refresh to load the data.
2. Create new data:
   Click 'Create' button, then it will direct to the create page.
   Fill in all information, then click 'Update'.
   Then it will return to home page with created data.
3. Edit data:
   Click 'Edit' link behind the entry you want to edit, then it will direct to the edit page.
   Make changes, then click 'Update'.
   Then it will return to home page with updated data.
4. Delete data:
   Click 'Del' link behind the entry you want to delete.
   It will refresh the home page with the data deleted.
  

Notice
=============
1. The file to upload should have following format:

   |TRAIN_LINE,ROUTE_NAME,RUN_NUMBER,OPERATOR_ID|
   ----------------------------------------------
   |El,BrownLine,E102,SJones|
   |Metra,UPN,M405,AJohnson|
   
2. Each data entry should have an unique run number, otherwise will be treated as duplication.
   You can only change run number by creating a new one.
3. Every form field for train data is required. 
   An empty field will result in system exception.
4. Sometimes data operation might not take effect immediatetly.
   You can refresh the page to get the result.
   

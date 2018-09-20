from SQLStatements import *

##//STEP I:
##//START HERE:
##// provide file location as a parameter to the function below. Replace all backslashes with forward slashes.
##// The function below will return FileLocation, # of Files available at location
##// and List of files at the specified location.
File_Information = (Count_Number_Of_Files("c:/Sudhir/Hotel_Submissions/Edited_DataFiles10272017"))

##// getting the list of files available at the specified location and assigning them to a list
##// for further processing.
fileInformation = File_Information[0]
fileList = File_Information[2] ##// this gives me the list of files available at the "File Location"

''' ## start of information segment
##// Loop through the list of files and perform the table operations
##// Step 1: Get table name from first part of file name e.g. FileName = "BD.txt" ==> Table Name is "BD" as you ignore the file extension
##// Step 2: Get headers from file (e.g. propcode, internationalhotelcode, csr_certified .....)
##// Step 3: If table exists, drop the table
##// Step 4: Use file headers to create SQL query for creation of table
##// Step 5: Get rest of file data excluding the headers from the file
##// Step 6: Generate SQL query to insert data into newly created table as above
##// Step 7: Insert file data into SQL database with table name = file name (without extension)
##// Step 8: Output information regarding file columns and rows and completion of insertion of data into table
##// Step 9: Repeat the process for the rest of the files in the filelist available at the location specified.
##// Step 10: print succcess message on completion of tasks.
end of information segment ##'''

##// STEP 2:
##// If files available at location perform further processing
if fileList:
   fileHandling(fileList,fileInformation)
else:
   ##// if no files are found at the specified location, the script will exit and print out the message below to the user.
   print("No Files Found")

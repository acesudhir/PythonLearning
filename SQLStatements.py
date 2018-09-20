import os
import os.path
import pyodbc
import csv
import re

'''
## // Function SQL Connector:
        return type: SQL connection object
'''
def sqlConnector():
    try:
        server = "<full path of local or remote database>"
        database = "<Database_Name>"
        username="<Create a pythonic user for such operations in SQL server first>"
        password="<Password>"
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
        return cnxn
    except Error as e:
        return (e)

'''
## // Function SqlDeleteTable:
        return type: None
        Action Performed: Drops table if table exists in database
'''
def sqlDeleteTable(cnxn,tableName):
    cursor=cnxn.cursor()
    print("******** Delete Existing Table********")
    cursor.execute("DROP TABLE "+tableName)
    print("******** Finished Deletion of Table********")
    cursor.commit()
    print("******** Commited Changes********")
    cursor.close()
    cnxn.close()

'''
## // Function checkTableExists:
        return type: Boolean (True/False)
        Action Performed: Checks if table exists in database
'''
def checkTableExists(dbcon, tableName):
    dbcur = dbcon.cursor()
    checkQuery = "select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME="+"'"+tableName+"'"
    tableCheck = dbcur.execute(checkQuery)
    result = dbcur.fetchall()
    if result:
       dbcur.close()
       dbcon.close()
       return True
    dbcur.close()
    return False


'''
## // Function sqlTableOperations:
        return type: String ("Process completed message")
        Action Performed: 
        1. gets filelist from location
        2. checks if table exists in database
        3. deletes existing table from database.
        4. Gets file headers and create sql query for creation of table with file headers as 
           column names and data type as VARCHAR(255)
        5. Gets rest of file data sans the headers and inserts into SQL database specified in the 
           SQL connector function. 
'''
def sqlTableOperations(fileList,fileInformation):
    for file in fileList:
        base = os.path.basename(fileInformation+"/"+file)
        tableName = os.path.splitext(base)[0] ##// getting only the filename without extension as tables in DB are created by firstpart of filename.
        existingTable = checkTableExists(sqlConnector(),tableName) ##// will check if table exists, and if it does, table will be deleted.
        if existingTable:
           sqlDeleteTable(sqlConnector(),tableName)##//delete table in database.
        ##//read source file from "fileLocation" drive
        print("********** Reading File **********")
        f1 = open(fileInformation+"/"+file, "r")
        print("File is: ",fileInformation+"/"+file)
        reader = csv.reader(f1,delimiter="\t")
        headers=next(reader)
        data=list(reader)
        print ("File Column & Row Count: ",len(headers),len(data))
        ##get header for creation of table
        ##// Generating SQL query based on headers and addition of column type.
        sqlStringHeader = str(headers).replace('[',"(")
        sqlStringHeader = str(sqlStringHeader).replace(']',"VARCHAR(255))")
        sqlStringHeader = str(sqlStringHeader).replace(","," VARCHAR(255),")
        sqlStringHeader = str(sqlStringHeader).replace("'"," ")
        ##//Create Table now
        dbConnector = sqlConnector()
        cursor = dbConnector.cursor()
        sqlQuery = "CREATE TABLE "+tableName+" "+sqlStringHeader
        cursor.execute(sqlQuery)
        cursor.commit()
        cursor.close()
        dbConnector.close()
        print("Finished table creation")

        ##// create connection for insertion of data.
        dbcon = sqlConnector()
        dbcur = dbcon.cursor()

        for row in data:
            ##// ensure columns with no data in it are given '' string in SQL query to be generated.
            rowData = [val if val else '' for val in row]+([''] * (len(headers) - len(row)))
            ##// replace "[" of list with "(" so entire sequence can be used as sql query.
            rowData = str(rowData).replace('[',"(")
            rowData = str(rowData).replace(']',")")
            rowQuery = "INSERT INTO "+tableName+" VALUES "+rowData
            dbcur.execute(rowQuery)
            dbcur.commit()
        print("Finished data insertion for : ",file)
        f1.close()
    dbcur.close()
    dbcon.close()
    print("Records succcessfully moved to Database")

'''
## // Function Count_Number_Of_Files:
        return type: String (File Location, # of files at location and list of files at location)
        Action Performed: returns information regarding location of files, count of files at location and the file names for further processing.
'''

def Count_Number_Of_Files(FileLocation):
    onlyfiles=next(os.walk(FileLocation))[2] # the [2] picks up only the files and ignores any subdirectory in the "FileLocation"
    FileCount = len(onlyfiles)
    List_of_Files = onlyfiles
    return (FileLocation,FileCount,List_of_Files)

'''
## // Function fileHandling:
        return type: String (process completion message)
        Action Performed: runs through all function calls as in SQLTableOperations function and prints process completion message.
'''

def fileHandling(fileList,fileInformation):
    ##// create sql tables and insert data from files.
    sqlTableOperations(fileList,fileInformation)
    return "Process Completed, Check Database for inserted records"

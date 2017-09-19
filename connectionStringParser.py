import csv
import argparse
import DotNetConnStrRegx



def getAppConnectionInfoList(filename,col,addColumns):
    connectionInfoList=[]
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        print("Ignoring the header row %s"%header_row)
        new_way(addColumns, col, connectionInfoList, reader)
    return connectionInfoList


def old_way(addColumns, col, connectionInfoList, reader):
    for row in reader:
        # column 6 has the connection string
        print row
        connStrLines = str(row[col]).lower().strip()
        print connStrLines
        connStr = DotNetConnStrRegx.extractConnectionString(connStrLines)
        print connStr
        if connStr is not None:
            # output = ""
            # for c in addColumns:
            #     output = row[c],output
            # print (output)
            source = BreakLinesInternally(str(connStr))
            if source is None:
                source = DotNetConnStrRegx.extractServerAndDatabaseName(str(connStr))
            if source is not None:
                important = tuple(source)

                appConnectionInfo = (row[addColumns], important[0], important[1])
                connectionInfoList.append(appConnectionInfo)

            else:
                print("Cannot extract the db info from the connection string %s" % connStr)
        else:

            print ("Connection String is not found!")

def new_way(addColumns, col, connectionInfoList,  reader):
    for row in reader:
        # column 6 has the connection string
        print row
        connStrLines = str(row[col]).lower().strip()
        for line in connStrLines.splitlines():
            # output = ""
            # for c in addColumns:
            #     output = row[c],output
            # print (output)
            source = DotNetConnStrRegx.extractInitialCatalogAndDataSource(line)
            if source is None:
                source = DotNetConnStrRegx.extractServerAndDatabaseName(line)
            if source is not None:
                important = tuple(source)

                appConnectionInfo = (row[addColumns], important[0], important[1])
                connectionInfoList.append(appConnectionInfo)

            else:
                print("Cannot extract the db info from the connection string %s" % line)
        else:

            print ("Connection String is not found!")
def WriteApplicationDbInfo_csv( outFile):

    with open(outFile, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['appName', 'server(instance)', 'dbname'])
        for t in appConnectionInfoList:
            writer.writerow([t[0], t[1], t[2]])


def BreakLinesInternally(input):
    db = []
    for line in input.splitlines():
        print("*****" + line)

        appConnection = extractInitialCatalogAndDataSource(line)
        if(appConnection!=None):
            db.append(appConnection)
            print db
    return db

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-file", help="full path to the csv file. Default is input.csv file in the current directory", type=str, default="input/appConnectionStringsScrape.csv")
    parser.add_argument("--column", help = "the 0 based position of the column", type=int, default=6)
    parser.add_argument("--add-col", help="position of the additional column to include in the output report", type=int, default=2)
    return parser.parse_args()
if __name__     == "__main__":

    args = parse_args()

    filename = args.csv_file
    column=args.column
    additionalColumns=args.add_col

    appConnectionInfoList = getAppConnectionInfoList(filename,column,additionalColumns)
    print(appConnectionInfoList)
    outFile = "appDbInfo.csv"
    WriteApplicationDbInfo_csv(outFile)


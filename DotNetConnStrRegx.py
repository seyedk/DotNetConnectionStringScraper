import re

from connectionStringParser import BreakLinesInternally

dataSourcetxt= """
<connectionStrings>
    <add name="PDSIPortalConnectionString" connectionString="Data Source=DC1AGL01D01;Initial Catalog=PDSIPortal;Integrated Security=True;" providerName="System.Data.SqlClient" />
    <add name="EligibilityPortalConnectionString" connectionString="data source=DC1AGL01D01; Initial Catalog=EligibilityPortal; Integrated Security=true;" providerName="System.Data.SqlClient" />
    <add name="BUSConnectionString" connectionString="data source=DC1AGL01D01; Initial Catalog=BUS; Integrated Security=true;" providerName="System.Data.SqlClient" />
    <add name="PDSConnectionString" connectionString="data source=DC1AGL01D01; Initial Catalog=PDS; Integrated Security=true; ApplicationIntent=ReadWrite; MultipleActiveResultSets=true" providerName="System.Data.SqlClient" />
    <add name="PDSConnectionStringRO" connectionString="data source=DC1AGL01D01; Initial Catalog=PDS; Integrated Security=true; ApplicationIntent=ReadOnly" providerName="System.Data.SqlClient" />
    <add name="PDSUI_PDSIPortalConnectionString" connectionString="Data Source=DC1AGL01D01;Initial Catalog=PDSIPortal;Integrated Security=True" providerName="System.Data.SqlClient" />
    <add name="HangfireConnectionString" connectionString="Data Source=DC1SQL02D02;Initial Catalog=HangFire;Integrated Security=True" providerName="System.Data.SqlClient" />
    <add name="PDS_Authentication_Module_Core__Db" connectionString="Data Source=DC1AGL01D01;Initial Catalog=PDSIPortal;Integrated Security=True;" providerName="System.Data.SqlClient" />
  </connectionStrings>
"""
serverTxt='server=dc1ag-l01p01;database=master-office;integrated security=true;'


multiValueTxt="""</appsettings>
	<connectionstrings>
	    <add name="pdsconnectionstring" connectionstring="data source=sc1agl01d01; initial catalog=pds; integrated security=true; applicationintent=readwrite" xdt:transform="setattributes(connectionstring)" xdt:locator="match(name)" /> 
	    <add name="pdsconnectionstringro" connectionstring="data source=afshin; initial catalog=ketabchi; integrated security=true; applicationintent=readonly" xdt:transform="setattributes(connectionstring)" xdt:locator="match(name)" />
	</connectionstrings>
	<log4net>
    	<appender name="adonetappender" type="log4net.appender.adonetappender">
      		<connectionstring name="adonetappenderconnstr" xdt:transform="setattributes(value)" xdt:locator="match(name)" value="data source=sc1agl01d01;initial catalog=logging;integrated security=true;" />
    	</appender>"""




def extractInitialCatalogAndDataSource(input):

    re1='(data)'	# Word 1
    re2='(\\s+)'	# White Space 1
    re3='(source)'	# Word 2
    re4='(=)'	# Any Single Character 1
    re5='((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'	# Alphanum 1p1
    re6='(-)*'                              # alphanum 1dash
    re7='((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'  # Alphanum 1p2
    re8='(;\\s*)'	# Any Single Character 2
    re9='(initial)'	# Word 3
    re10='(\\s+)'	# White Space 2
    re11='(catalog)'	# Word 4
    re12='(=)'	# Any Single Character 3
    re13='((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'	# alphanum 2p1
    re14 = '(-)*'                           # alphanum 2dash
    re15= '(_)*'
    re16 = '((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'  # Alphanum 2p2
    re17='(;)'	# Any Single Character 4

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11+re12+re13+re14+re15+re16+re17,re.IGNORECASE|re.DOTALL)
    m = rg.search(input)
    if m:
        word1=m.group(1)
        ws1=m.group(2)
        word2=m.group(3)
        c1=m.group(4)
        alphanum1p1=m.group(5)
        alphanum1dash=m.group(6) if m.group(6) !=None else ""
        alphanum1p2=m.group(7) if m.group(7) !=None else ""
        ws2=m.group(8)
        word4=m.group(9)
        c3=m.group(10)
        c4=m.group(11)
        c5=m.group(12)
        alphanum2p1=m.group(13)
        alphanum2dash=m.group(14) if m.group(14) != None else ""
        alphanum2dash=m.group(15) if m.group(15) != None else ""

        alphanum2p2 = m.group(16) if m.group(16) != None else ""

        alphanum3=m.group(17)

        return (alphanum1p1+alphanum1dash + alphanum1p2,alphanum2p1+alphanum2dash+alphanum2p2)
    else:
        return None


def extractConnectionString(txt):
    re1 = '.*?'  # Non-greedy match on filler
    re2 = '(add)'  # Word 1
    re3 = '.*?'  # Non-greedy match on filler
    re4 = '(name)'  # Word 2
    re5 = '.*?'  # Non-greedy match on filler
    re6 = '(".*?")'  # Double Quote String 1
    re7 = '(\\s+)'  # White Space 1
    re8 = '((?:[a-z][a-z]+))'  # Word 3
    re9 = '.*?'  # Non-greedy match on filler
    re10 = '(".*?")'  # Double Quote String 2

    rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
    m = rg.search(txt)
    if m:
        word1 = m.group(1)
        word2 = m.group(2)
        string1 = m.group(3)
        ws1 = m.group(4)
        word3 = m.group(5)
        connectionString = m.group(6)
        return connectionString
    else:
        return None


def extractServerAndDatabaseName2(input):
    """ It goes here"""

    re1='(server)'	# Word 1
    re2='(=)'	# Any Single Character 1
    re3='((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'	# Alphanum 1
    re4='(;)'	# Any Single Character 2
    re5='(database)'	# Word 2
    re6='(=)'	# Any Single Character 3
    re7='((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'	# Alphanum 2
    re8='(;)'	# Any Single Character 4

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m = rg.search(str(input).strip('"'))
    if m:
        word1=m.group(1)
        c1=m.group(2)
        alphanum1=m.group(3)
        c2=m.group(4)
        word2=m.group(5)
        c3=m.group(6)
        alphanum2=m.group(7)
        c4=m.group(8)
        return [alphanum1,alphanum2]
    else:
        return None

def extractServerAndDatabaseName(input):
    """ It goes here"""

    re1 = '(server)'  # Word 1
    re2 = '(=)'  # Any Single Character 1
    re3 = '((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'  # a1p1
    re4 = '(-)*'                                # a1d
    re5 = '((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'    # a1p1

    re6 = '(;)'  # Any Single Character 2
    re7 = '(database)'  # Word 2
    re8 = '(=)'  # Any Single Character 3
    re9 = '((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'  # a2p1
    re10 = '(-)*'                             # a2d
    re11 = '((?:[a-z][a-z]*[0-9]*[a-z0-9]*))'  # a2p2
    re12 = '(;)'  # Any Single Character 4

    rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8+re9+re10+re11+re12, re.IGNORECASE | re.DOTALL)
    m = rg.search(str(input).strip('"'))
    if m:
        word1 = m.group(1)
        c1 = m.group(2)
        a1p1 = m.group(3)
        a1d = m.group(4) if m.group(4) != None else ""
        a1p2 = m.group(5) if m.group(5) != None else ""

        c3 = m.group(6)
        c4 = m.group(7)
        c5 = m.group(8)

        a2p1 = m.group(9)
        a2d = m.group(10) if m.group(10)!=None else ""
        a2p2 = m.group(11) if m.group(11)!=None else ""
        c6 = m.group(12)
        return [a1p1+a1d+a1p2, a2p1+a2d+a2p2]
    else:
        return None
if __name__ == '__main__':
    # db = extractServerAndDatabaseName(serverTxt)
    # print db
    # db = extractInitialCatalogAndDataSource(dataSourcetxt)
    # print db

    db = BreakLinesInternally(dataSourcetxt)
    print db

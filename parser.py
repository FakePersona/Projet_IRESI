import re

pattern = {}



# epahttp syntax :
# host [D:H:M:S] "request" code size
pattern["epahttp"] = re.compile("""
(?P<host>.*)
\s\[
(?P<D>[0-9]*)
:
(?P<H>[0-9]*)
:
(?P<M>[0-9]*)
:
(?P<S>[0-9]*)
\]\s"
(?P<request>.*)
"\s
(?P<code>[0-9]*)
\s
(?P<size>[0-9]*)
""", re.VERBOSE)



# sdschttp syntax :
# hostNetwork+host: dayName monthName D H:M:S Y (fileName): operation: "remainder
pattern["sdschttp"] = re.compile("""
(?P<hostNetwork>[0-9]*)
\+
(?P<host>[0-9]*)
:\s
(?P<dayName>[A-Z][a-z][a-z])
\s
(?P<monthName>[A-Z][a-z][a-z])
\s
(?P<D>[0-9]*)
\s
(?P<H>[0-9]*)
:
(?P<M>[0-9]*)
:
(?P<S>[0-9]*)
\s
(?P<Y>[0-9]*)
\s\(
(?P<fileName>.*)
\):\s
(?P<operation>.*)
:\s "
(?P<remainder>.*)
""", re.VERBOSE)



# calgaryhttp syntax :
# host - - [D/monthName/Y:H:M:S timeZone] "fileName" code size
pattern["calgaryhttp"] = re.compile("""
(?P<host>local|remote)
\s-\s-\s\[
(?P<D>[0-9]*)
/
(?P<monthName>[A-Z][a-z][a-z])
/
(?P<Y>[0-9]*)
:
(?P<H>[0-9]*)
:
(?P<M>[0-9]*)
:
(?P<S>[0-9]*)
\s
(?P<timeZone>-[0-9]*)
\]\s"
(?P<fileName>.*)
"\s
(?P<code>[0-9]*)
\s
(?P<size>[0-9]*)

""", re.VERBOSE)





# t in {"epahttp", "sdschttp", "calgaryhttp"}
def parseString(string, t):
    return pattern[t].match(string)




# t in {"epahttp", "sdschttp", "calgaryhttp"}
# Returns a list. Each element of the list is a re.match object, representing a line of the file.
# Use "group" method to access to items 
#
# ex : to access to the day (D) of the 42nd line of the file "toto.txt", using "epahttp" syntax :
# data = parseFile("toto.txt", "epahttp")
# data[42].group("D")

def parseFile(path, t):
    f = open(path, encoding = "ISO-8859-1")
    data = []
    for line in f:
        data.append(parseString(line, t))
    return data



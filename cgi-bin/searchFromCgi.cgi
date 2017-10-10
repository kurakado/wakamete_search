#!/usr/bin/python3

import cgi
import sys

from searchData import search
from RoleEnum import Role,returnRole,returnString


form = cgi.FieldStorage()
#print(dir(form))
print('Content-type: text/html; charset=UTF-8\r\n')
print("""
<html>
  <head>
  <title></title>
  </head>
  <body>
""")
if "trip" in form.keys():
    ret=search(form["trip"].value)
    print("HIT {} </br>".format(len(ret)))
    print("<table>")
    for line in ret:
        village_num=line[0]
        CN=line[2]
        role=returnString(Role(line[5]))
        print("<tr><td><a href='http://jinrou.dip.jp/~jinrou/kako/{}.html'>{}番地</a></td><td> CN：{}</td><td> 役職：{} </td></tr>".format(village_num, village_num, CN , role) )
    print("</table>")

elif len(sys.argv) > 1:
    ret=search(sys.argv[1])
    print("HIT {}".format(len(ret)))
    for line in ret:
        village_num=line[0]
        CN=line[2]
        role=returnString(Role(line[5]))
        print("{}番地 CN：{} 役職：{}".format(village_num, CN , role) )

else:
    print("please give me a trip.")

print("""
  </body>
</html>""")

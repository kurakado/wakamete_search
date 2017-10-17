from time import sleep
import urllib.request
import sys

baseurl="http://jinrou.dip.jp/~jinrou/kako/"
sleepTime=0.1
htmlDataDir="../village_data/"

if len(sys.argv)<3:
    print("input error: {} <start> <end>".format(sys.argv[0]))
    sys.exit(1)

for village_num in range( int(sys.argv[1]),int(sys.argv[2])+1):
#    print(village_num)
    url=baseurl+"{}.html".format(village_num)
    try:
        urllib.request.urlretrieve(url,"{}{}.html".format(htmlDataDir,village_num))
        print("get {}".format(village_num))
    except:
        pass
    finally:
        sleep(sleepTime)

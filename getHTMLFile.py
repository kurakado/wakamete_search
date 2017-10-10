from time import sleep
import urllib.request
import sys

baseurl="http://jinrou.dip.jp/~jinrou/kako/"
sleepTime=0.1
htmlDataDir="./village_data/"

for village_num in range(139311,150787+1):
#    print(village_num)
    url=baseurl+"{}.html".format(village_num)
    try:
        urllib.request.urlretrieve(url,"{}{}.html".format(htmlDataDir,village_num))
        print("get {}".format(village_num))
    except:
        pass
    finally:
        sleep(sleepTime)

if [ $# -ge 2 ]
then
    start=$1
    end=$2
else
    echo "please input start_village_number"
    read start
    echo "please input end_village_number"
    read end
    echo "getHTMLFile.py $start $end"
    getHTMLFile.py $start $end
fi

for num in `seq $start $end`
do
  nkf -w --overwrite ../village_data/${num}.html
  #echo "nkf -w --overwrite ../village_data/${num}.html"
done

for i in `seq 1 10`
do
   echo $i
   top -l 1 > $i.txt
   #top -bn1 > $i.txt
   sleep 60
done

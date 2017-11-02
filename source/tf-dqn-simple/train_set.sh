for i in `seq 1 10`
do
    echo "Maximum node : "$i
    for j in `seq 5 10`
    do
        echo "Time constraint : "$j
        python train.py $i $j
    done
done
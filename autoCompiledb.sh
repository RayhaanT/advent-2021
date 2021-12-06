for i in `seq 1 $1`
do
    compiledb make day="$i"
done

make day=$1
if [ "$2" == "gdb" ]
then
    gdb ./out$1
else
    ./out$1
fi 

while :
do
   _line=`docker stats | sudo`
   _date=`date '+%Y/%m/%d %H:%M:%S'`
   echo ""${_date} ${_line}"" >> free.log
   sleep 1
done

#!/bin/sh
while true;
do
        echo $(date +%H:%M:%S.%5N),$(nvidia-smi dmon -s p -c 1 | tail -1 | awk '{print $2}') >> /tmp/$1.log
        #| awk '{print $4}' >> /tmp/$1.log
done

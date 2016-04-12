#!/bin/bash
blackListFile=/root/denyCC/blackLists.data
dropedIPS=/root/denyCC/drop.data
logFile=/root/denyCC/drop.log
dev=em2
startTime=30
offSet=1
[ -d "/root/denyCC" ]||(mkdir /root/denyCC&&touch /root/denyCC/{blackListFile,drop.data,drop.log})
netstat -anpt|egrep "10.10.10.10:80"|awk '/TIME_WAIT/{print $5}'|awk -F: '{s[$1]++}END{for(i in s){if(s[i] > 0){print i}}}' > $blackListFile

bips=`cat $blackListFile`

if [ -z "$bips" ];then
    dips=`cat $dropedIPS`
    if [ -z "$dips" ];then
        exit 0
    else
        for ip in $dips
        do
            dtime=`echo $ip|awk -F: '{print $1}'`
            dip=`echo $ip|awk -F: '{print $2}'`
            if [ $dtime -eq 0 ];then
                iptables -D INPUT -i $dev -s $dip -j DROP
                sed -i "/${dtime}:${dip}/d" $dropedIPS
                echo "`date +%Y/%m/%d\ %T` Delete $dip  from iptables and datafile" >> $logFile
            else
                oldTime=$dtime
                let dtime-=$offSet
                sed -i "s/${oldTime}:${dip}/${dtime}:${dip}/g" $dropedIPS
                echo "`date +%Y/%m/%d\ %T` Reduce block time from $oldTime to $dtime for $dip" >> $logFile
            fi
        done
    fi
else
    dips=`cat $dropedIPS`
    for ip in $bips
    do
        if [ -z "$dips" ];then
            iptables -I INPUT -i $dev -s $ip -j DROP
            echo "${startTime}:${ip}" >> $dropedIPS
            echo "`date +%Y/%m/%d\ %T` Add $ip in iptables and datafile" >> $logFile
        else
            for dip in $dips
            do
                dtime=`echo $dip|awk -F: '{print $1}'`
                dip=`echo $dip|awk -F: '{print $2}'`
                if [ "$ip" != "$dip" ];then
                    iptables -I INPUT -i $dev -s $ip -j DROP
                    echo "${startTime}:${ip}" >> $dropedIPS
                    echo "`date +%Y/%m/%d\ %T` Add $dip in iptables and datafile" >> $logFile
                    if [ $dtime -eq 0 ];then
                        iptables -D INPUT -i $dev -s $dip -j DROP
                        sed -i "/0:${dip}/d" $dropedIPS
                        echo "`date +%Y/%m/%d\ %T` Block time for $dip is $dtime durying the checking,so delete $ip in iptables and datafile" >> $logFile
                    else
                        oldTime=$dtime
                        let dtime-=$offSet
                        sed -i "s/${oldTime}:${dip}/${dtime}:${dip}/g" $dropedIPS
                        echo "`date +%Y/%m/%d\ %T` Reduce block time from $oldTime to $dtime for $dip" >> $logFile
                    fi
                else
                    sed -i "s/${dtime}:$dip/${startTime}:${dip}/g" $dropedIPS
                    echo "`date +%Y/%m/%d\ %T` $ip comes again,so readd it to the iptables and datafile" >> $logFile
                fi 
            done
        fi
    done
fi

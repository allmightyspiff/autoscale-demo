#!/bin/bash

DOMAIN="cgallo.com"
DC="hou02"
IMAGE="1470578f-2a72-46a0-b082-ade30ac6be48"

KEYNAME="cgalloKey"
POSTINST="https://raw.githubusercontent.com/allmightyspiff/autoscale-demo/master/startup.sh"
echo -e "\e[32mRunning:\e[0m slcli vs create --datacenter=${DC} --hostname=vpx-node --domain=\e[36m${DOMAIN}\e[0m --billing hourly --key=\e[36m${KEYNAME}\e[0m --cpu=1 --memory=1024 --image=${IMAGE} --postinstall=${POSTINST}" 

slcli --really vs create --datacenter=${DC} --hostname=vpx-node --domain=${DOMAIN} --billing hourly --key=${KEYNAME} --cpu=1 --memory=1024 --image=${IMAGE} --postinstall=${POSTINST} > /var/log/minion01.log

VSID=`cat /var/log/minion01.log | grep "^id " | awk '{print $2}'`
sleep 10

echo -e "\e[32mRunning:\e[0m slcli vs detail ${VSID} "
slcli vs detail ${VSID}

echo -e "\e[93mWaiting for instance to come online...\e[0m"

LOOP=0
while [ $LOOP -eq 0 ]
do
    STATUS=`slcli vs detail ${VSID} | grep active_transaction | awk '{print $2}'`
    OWNER=`slcli vs detail ${VSID} | grep active_transaction | awk '{print $2}'`
    if [ "$STATUS" = "NULL" ] && [ "$OWNER" != "NULL" ]
    then 
        echo -e "\e[32mInstance is ready\e[0m"
        LOOP=1
    else
        COUNTER=0
        spin='-\|/'
        echo -e "\e[93mNot ready yet. Status: ${STATUS}\e[32m"
        while [ $COUNTER -lt 40 ]
        do
            i=$(( COUNTER %4 ))
            printf "\r${spin:$i:1}"
            sleep .20
            COUNTER=$[$COUNTER+1]

        done
        echo -ne "\b\e[0m"
    fi
done


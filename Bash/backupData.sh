setglobal(){
	export PATH=${PWD}/../bin:$PATH
	export FABRIC_CFG_PATH=$PWD/../config/
	export CORE_PEER_TLS_ENABLED=true
	export CORE_PEER_LOCALMSPID="Org1MSP"
	export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.jwclab.com/peers/peer0.org1.jwclab.com/tls/ca.crt
	export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.jwclab.com/users/Admin@org1.jwclab.com/msp
	export CORE_PEER_ADDRESS=localhost:7051
	export ORDERER_ADDRESS=localhost:7050
	export PEERS="peer0.org1"
	export CHANNEL_NAME="mychannel"
	export TLSCACERT=${PWD}/organizations/ordererOrganizations/jwclab.com/orderers/orderer.jwclab.com/msp/tlscacerts/tlsca.jwclab.com-cert.pem
	export ORG1CACERT=${PWD}/organizations/peerOrganizations/org1.jwclab.com/peers/peer0.org1.jwclab.com/tls/ca.crt
	export ORG2CACERT=${PWD}/organizations/peerOrganizations/org2.jwclab.com/peers/peer0.org2.jwclab.com/tls/ca.crt
}

compareHashFromBlockchain(){
	setglobal
	check='false'
	measurement=$1
	hash_query=`peer chaincode query -C mychannel -n iot -c '{"function":"QueryRecordHistoryByTimeRange","Args":["'$measurement'","2020-09-16T00:00:00Z","2020-09-17T00:00:00Z"]}'`
	hash_query=${hash_query//',{'/' {'}
	hash_query=${hash_query//'['/''}
	hash_query=${hash_query//']'/''}
	IFS=' '
	read -a hash_arr <<< "$hash_query"
	for hash in "${hash_arr[@]}";
	do
		# printf "$hash\n"
		IFS=',' read -a json_body <<< "${hash}"
		json_body[2]=${json_body[2]//'":"'/'" "'}
		IFS=' ' read -a data <<< "${json_body[2]}"
		blockchain_hash=`echo ${data[1]} | cut -c2-33`
		dateTime=`echo ${data[0]} | cut -c10-65`
		dateTime=${dateTime//'--'/' '}
		IFS=' ' read -a dateTime_arr <<< "${dateTime}"
		# printf "$measurement ${dateTime_arr[0]} ${dateTime_arr[1]}\n"
		influxdb_hash=`python3 /home/mau/PycharmProjects/envmonitoring/compareHash.py $measurement ${dateTime_arr[0]} ${dateTime_arr[1]}`
		# echo "$blockchain_hash $influxdb_hash"
		if [ "$influxdb_hash" == "$blockchain_hash" ]; then 
			check="true"
		else
			check="false"
			break
		fi
	done
	echo $check
}

mode=$1
host="178.128.107.247:8088"

while [ true ]; 
do
	if [ "$mode" == "test" ]; then
	echo "test"
	elif [ "$mode" == "backup" ];then
		dateTime=`date -u +%H:%M`
		echo $dateTime
		if [ "$dateTime" == "08:58" ];then
			databases=$(python3 /home/mau/PycharmProjects/envmonitoring/getNumberOfStations.py)
			IFS=' ' read -a database_arr <<< "${databases}"
			for database in "${database_arr[@]}";
			do
				measurement=$(python3 /home/mau/PycharmProjects/envmonitoring/getDeviceId.py $database)
				flag=$(compareHashFromBlockchain $measurement)
				# echo $flag
				now=`date '+%Y-%m-%dT00:00:00Z'`
				yesterday=`date -d '1 day ago' '+%Y-%m-%dT00:00:00Z'`
				if [ "$flag" = "true" ];then
					echo "Backup data from $measurement database"
					influxd backup -portable -database $measurement -host $host -start $yesterday -end $now /tmp/backup/$measurement/
				else
					echo "Error when compare hash!!!"
				fi
			done
		fi
		sleep 60
	elif [ "$mode" == "restore" ];then
		echo "Restore"
		# influxd restore -portable -host 178.128.107.247:8088 -db haichau_stations -newdb haichau_bak /tmp/backup/
	else 
		echo "Invalid mode!"
		echo "Mode: test--backup--restore"
		exit 0
	fi
done








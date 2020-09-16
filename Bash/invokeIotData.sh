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

chaincodeInvokeFiltered() {
	echo 
	echo "========== Invoke transaction iotdata ================"
	echo
	for i in {0..11}
	do
		python filterData.py
		sleep 4.8
	done
	md5_hash=$(python3 /home/mau/PycharmProjects/filterDataIOT/hashIotDataFiltered.py)
	echo $md5_hash
	# echo $data
	# set -x
	peer chaincode invoke -o $ORDERER_ADDRESS --ordererTLSHostnameOverride orderer.jwclab.com --tls --cafile $TLSCACERT -C mychannel -n iot --peerAddresses localhost:7051 --tlsRootCertFiles $ORG1CACERT --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2CACERT -c '{"function":"AddRecord","Args":["'${md5_hash//'"'/'\"'}'"]}' >&log.txt
	# peer chaincode invoke -o $ORDERER_ADDRESS --ordererTLSHostnameOverride orderer.jwclab.com --tls --cafile $TLSCACERT -C mychannel -n iot --peerAddresses localhost:7051 --tlsRootCertFiles $ORG1CACERT --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2CACERT -c '{"function":"AddRecord","Args":["{\"id\":\"101\", \"dateTime\":\"2020-09-10T14:12:13\", \"data\":{\"TMP\":10, \"DUST\":10, \"HUM\":10, \"UV\":10, \"PH\":10}}"]}' >&log.txt
	# set +x
	cat log.txt
	echo "===================== Invoke transaction successful on $PEERS on channel '$CHANNEL_NAME' ===================== "
}

chaincodeInvokeNoFiltered() {
	echo 
	echo "========== Invoke transaction iotdata ================"
	echo
	md5_hash=$(python3 /home/mau/PycharmProjects/envmonitoring/hashIotDataNoFiltered.py)

	IFS=' '
	read -a md5_hash_arr <<< "$md5_hash"

	for hash in "${md5_hash_arr[@]}";
	do
	printf "$hash\n"
	# set -x
	peer chaincode invoke -o $ORDERER_ADDRESS --ordererTLSHostnameOverride orderer.jwclab.com --tls --cafile $TLSCACERT -C mychannel -n iot --peerAddresses localhost:7051 --tlsRootCertFiles $ORG1CACERT --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2CACERT -c '{"function":"AddRecord","Args":["'${hash//'"'/'\"'}'"]}' >&log.txt
	# peer chaincode invoke -o $ORDERER_ADDRESS --ordererTLSHostnameOverride orderer.jwclab.com --tls --cafile $TLSCACERT -C mychannel -n iot --peerAddresses localhost:7051 --tlsRootCertFiles $ORG1CACERT --peerAddresses localhost:9051 --tlsRootCertFiles $ORG2CACERT -c '{"function":"AddRecord","Args":["{\"id\":\"101\", \"dateTime\":\"2020-09-10T14:12:13\", \"data\":{\"TMP\":10, \"DUST\":10, \"HUM\":10, \"UV\":10, \"PH\":10}}"]}' >&log.txt
	set +x
	cat log.txt
	echo "===================== Invoke transaction successful on $PEERS on channel '$CHANNEL_NAME' ===================== "
	done
}

mode=$1

while [ true ]; do
	if [ "$mode" == "filter" ]; then
		peer channel getinfo -c mychannel
		chaincodeInvokeFiltered
		# peer chaincode query -C mychannel -n iot -c '{"function":"QueryRecord","Args":["101"]}'
	elif [ "$mode" == "nofilter" ];then
		# peer channel getinfo -c mychannel
		chaincodeInvokeNoFiltered 
		# peer chaincode query -C mychannel -n iot -c '{"function":"QueryRecord","Args":["103"]}'
		sleep 60
	elif [ "$mode" == "query" ];then
		# peer channel getinfo -c mychannel
		# peer chaincode query -C mychannel -n iot -c '{"function":"QueryRecordHistory","Args":["101"]}'
		peer chaincode query -C mychannel -n iot -c '{"function":"QueryRecordHistoryByTimeRange","Args":["101","2020-09-16T00:00:00Z","2020-09-17T00:00:00Z"]}'
	elif [ "$mode" == "test" ];then
		echo "test"
		
	else 
		echo "Invalid mode!"
		echo "Mode: filter--nofilter--query--test"
		exit 0
	fi
	
done




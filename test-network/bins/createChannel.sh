#for org1
export CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/users/Admin@org1.jwclab.com/msp

peer channel create -o $ORDERER_ADDRESS -c mychannel -f ./channel-artifacts/mychannel.tx --outputBlock ./channel-artifacts/mychannel.block

peer channel join -b ./channel-artifacts/mychannel.block -o $ORDERER_ADDRESS

peer channel update -f ./channel-artifacts/Org1MSPanchors.tx -c mychannel -o $ORDERER_ADDRESS


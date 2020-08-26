#for org2

export CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/users/Admin@org2.jwclab.com/msp

peer channel fetch 0 ./channel-artifacts/mychannel.block -o $ORDERER_ADDRESS -c mychannel

peer channel join -b ./channel-artifacts/mychannel.block -o $ORDERER_ADDRESS

peer channel update -f ./channel-artifacts/Org2MSPanchors.tx -c mychannel -o $ORDERER_ADDRESS
PATH=${PWD}/../bin:$PATH
FABRIC_CFG_PATH=${PWD}/configtx

if [ -d "organizations/peerOrganizations" ]; then
	rm -Rf organizations/peerOrganizations && rm -Rf organizations/ordererOrganizations
fi

echo "Register and enroll"
./organizations/fabric-ca/registerEnroll.sh

echo "Generate CCP file"
./organizations/ccp-generate.sh

echo "#########  Generating Orderer Genesis block ##############"
configtxgen -profile TwoOrgsOrdererGenesis -channelID system-channel -outputBlock ./system-genesis-block/genesis.block

if [ ! -d "channel-artifacts" ]; then
	mkdir channel-artifacts
fi

echo "Create channeltx"
configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/${CHANNEL_NAME}.tx -channelID $CHANNEL_NAME

echo "Create anchorpeer"
echo
echo "#######    Generating anchor peer update transaction for org1msp  ##########"
configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP
echo
echo "#######    Generating anchor peer update transaction for org2msp  ##########"
configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org2MSP


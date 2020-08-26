ORG=$1
/bin/bash ./organizations/fabric-ca/registerEnroll.sh 
echo " "
echo "#########  Generating CCP file ##############"
echo " "
/bin/bash ./organizations/ccp-generate.sh 
echo " "
echo "#########  Done. ##############"
echo " "
echo " "
echo "#########  Generating Orderer Genesis block ##############"
echo " "
configtxgen -profile TwoOrgsOrdererGenesis -channelID system-channel -outputBlock ./system-genesis-block/genesis.block 
echo " "
echo "######### Create channeltx ##########"
echo " "
configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./channel-artifacts/mychannel.tx -channelID mychannel
echo " "
echo "######### Create channeltx ##########"
echo " "
configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID mychannel -asOrg Org1MSP
echo " "
echo "#########  Done. ##############"
echo " "
exit 0
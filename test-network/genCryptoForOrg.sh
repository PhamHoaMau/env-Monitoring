ORG=$1
export FABRIC_CFG_PATH=$PWD/configtx/
export PATH=$PWD/../bin:$PATH
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
if [ $ORG == 1 ]; then
    configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org1MSPanchors.tx -channelID mychannel -asOrg Org1MSP
elif [ $ORG == 2 ]; then
    configtxgen -profile TwoOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/Org2MSPanchors.tx -channelID mychannel -asOrg Org2MSP
else
    echo "Orderer Org"
fi
echo " "
echo "#########  Done. ##############"
echo " "
exit 0
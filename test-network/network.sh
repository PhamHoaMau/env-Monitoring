# Print the usage message
function printHelp() {
  echo "Usage: "
  echo "  network.sh <Mode> "
  echo "  Modes:"
  echo "     setContext ------> set FABRIC_CFG_PATH + CORE_PEER_MSPCONFIGPATH"
  echo "     createChannel -----> create channel + joinchannel + update anchorpeer "
  echo "     fetchChannel -----> fetch channel + joinchannel + update anchorpeer "
  echo "     install ----> package + install + approvemyorg chaincode definition"
  echo "     commit ----> commit chaincode definition"
  echo "     querycommitted ----> querycommitted chaincode definition"
  echo "     invokeinit ----> invokeinit chaincode"
  echo "     addrecord ----> addrecord chaincode"
  echo "     query ----> query chaincode"
  echo "     export CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/users/Admin@org1.jwclab.com/msp"
  echo
}
function cc_get_package_id {  
    OUTPUT=$(peer lifecycle chaincode queryinstalled -O json)
    PACKAGE_ID=$(echo $OUTPUT | jq -r ".installed_chaincodes[]|select(.label==\"$LABEL\")|.package_id")
}

function setContext() {
  org=$1
  export FABRIC_CFG_PATH=${PWD}/configtx
  export CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/users/Admin@org1.jwclab.com/msp
}

function createChannel() {
  echo "Create channeltx"
  peer channel create -o $ORDERER_ADDRESS -c mychannel -f ./channel-artifacts/mychannel.tx --outputBlock ./channel-artifacts/mychannel.block
  
  echo "Join Channel"
  peer channel join -b ./channel-artifacts/mychannel.block -o $ORDERER_ADDRESS
  
  echo "Update anchorpeer"
  peer channel update -f ./channel-artifacts/Org1MSPanchors.tx -c mychannel -o $ORDERER_ADDRESS
}

function fetchChannel() {
  echo "Fetch channel"
  peer channel fetch 0 ./channel-artifacts/mychannel.block -o $ORDERER_ADDRESS -c mychannel

  echo "Join channel"
  peer channel join -b ./channel-artifacts/mychannel.block -o $ORDERER_ADDRESS
  
  echo "Update channel"
  peer channel update -f ./channel-artifacts/Org2MSPanchors.tx -c mychannel -o $ORDERER_ADDRESS
}


function installChainCode() {
  echo "Create package directory"
  mkdir -p /etc/hyperledger/fabric/packages
  echo
  echo "install go by apk"
  apk update && apk add --no-cache git make musl-dev go jq vim && rm -rf /var/cache/apk/
  echo
  echo "Package chaincode definition"
  peer lifecycle chaincode package $CC2_PACKAGE_FOLDER/$PACKAGE_NAME -p $CC_PATH --label=$LABEL -l $CC_LANGUAGE
  echo
  echo "Install chaincode definition"
  peer lifecycle chaincode install ${CC2_PACKAGE_FOLDER}/${PACKAGE_NAME}
  echo
  echo "Query installed"
  peer lifecycle chaincode queryinstalled
  cc_get_package_id
  echo
  echo "Approve for myorg"
  peer lifecycle chaincode approveformyorg --channelID $CC_CHANNEL_ID --name $CC_NAME --version $CC_VERSION --package-id $PACKAGE_ID --sequence $CC2_SEQUENCE --init-required -o $ORDERER_ADDRESS
  echo
  echo "Check commit readiness"
  peer lifecycle chaincode checkcommitreadiness --channelID $CC_CHANNEL_ID --name ${CC_NAME} --version ${CC_VERSION} --sequence 1 --init-required --output json
}

function commitChaincode() {
  echo 
  echo "commit chaincode definition"
  peer lifecycle chaincode commit -o $ORDERER_ADDRESS --channelID $CC_CHANNEL_ID --name $CC_NAME --version $CC_VERSION --sequence 1 --peerAddresses peer0.org1.jwclab.com:7051 --peerAddresses peer0.org2.jwclab.com:9051 --init-required --waitForEvent

  echo 
  echo "Query committed"
  peer lifecycle chaincode querycommitted --channelID mychannel
}

function querycommittedChaincode() {
  echo 
  echo "Query committed"
  peer lifecycle chaincode querycommitted --channelID mychannel
}

function invokeInitChaincode() {
  echo
  echo "Invode init chaincode"
  peer chaincode invoke -o $ORDERER_ADDRESS --channelID $CC_CHANNEL_ID --name $CC_NAME \
   --peerAddresses peer0.org1.jwclab.com:7051 --peerAddresses peer0.org2.jwclab.com:9051 \
   --isInit -c $CC_CONSTRUCTOR
}

function addRecord() {
  echo
  echo "Add record --> chaincode"
  peer chaincode invoke -o $ORDERER_ADDRESS --channelID $CC_CHANNEL_ID --name $CC_NAME \
   --peerAddresses peer0.org1.jwclab.com:7051 --peerAddresses peer0.org2.jwclab.com:9051 \
   -c '{"function":"AddRecord","Args":["{\"id\":\"DANANG_1\", \"dateTime\":\"2020-11-02 15:04:05\", \"data\":{\"ph\":7, \"hum\":12, \"dust\":1, \"uv\":1, \"tem\":30}}"]}'
}

function queryChaincode() {
  peer chaincode query --channelID $CC_CHANNEL_ID --name $CC_NAME -c $CC_QUERY
}

MODE=$1
ORG=$2
 
if [ "${MODE}" == "setContext" ]; then
  setContext $ORG
elif [ "${MODE}" == "createChannel" ]; then
  createChannel
elif [ "${MODE}" == "fetchChannel" ]; then
  fetchChannel
elif [ "${MODE}" == "intall" ]; then
  installChainCode
elif [ "${MODE}" == "commit" ]; then
  commitChaincode
elif [ "${MODE}" == "querycommitted" ]; then
  querycommittedChaincode
elif [ "${MODE}" == "invokeinit" ]; then
  invokeInitChaincode
elif [ "${MODE}" == "addrecord" ]; then
  addRecord
elif [ "${MODE}" == "query" ]; then
  queryChaincode
else
  printHelp
  exit 1
fi

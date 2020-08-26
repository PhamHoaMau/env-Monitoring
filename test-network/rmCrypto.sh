echo "Remove material"
rm -rf ./organizations/ordererOrganizations/ 
rm -rf ./organizations/peerOrganizations/
echo "Remove Crypto"
rm -rf ./system-genesis-block/genesis.block
rm -rf ./channel-artifacts/*.tx
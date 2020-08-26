echo "=====Stop container======="
docker stop orderer.jwclab.com

echo "=====Remove container======="
docker rm orderer.jwclab.com

echo "Create container orderer.jwclab.com "
docker run --env-file /home/mau/env-Monitoring/test-network/env.txt -v /home/mau/env-Monitoring/test-network/system-genesis-block/genesis.block:/var/hyperledger/orderer/orderer.genesis.block -v /home/mau/env-Monitoring/test-network/organizations/ordererOrganizations/jwclab.com/orderers/orderer.jwclab.com/msp:/var/hyperledger/orderer/msp -v /home/mau/env-Monitoring/test-network/organizations/ordererOrganizations/jwclab.com/orderers/orderer.jwclab.com/tls/:/var/hyperledger/orderer/tls -v /home/mau/env-Monitoring/test-network/channel-artifacts/:/var/hyperledger/orderer/channel-artifacts --name orderer.jwclab.com --network jwcnetwork -p 7050:7050 -itd hyperledger/fabric-orderer:2.2.0

docker network inspect jwcnetwork 

docker exec -ti peer0.org1.jwclab.com sh
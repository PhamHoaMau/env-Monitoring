echo "=====Stop container======="
docker stop peer0.org2.jwclab.com 

echo "=====Remove container======="
docker rm peer0.org2.jwclab.com 

echo "Create container peer0.org2.jwclab.com "
docker run --env-file /home/mau/env-Monitoring/test-network/env2.txt -v /home/mau/env-Monitoring/test-network/network.sh:/etc/hyperledger/fabric/network.sh -v /home/mau/env-Monitoring/test-network/organizations/peerOrganizations/org2.jwclab.com/connection-org2.json:/etc/hyperledger/fabric/connection-org2.json -v /var/run/:/host/var/run/ -v /home/mau/env-Monitoring/test-network/organizations/peerOrganizations/org2.jwclab.com/peers/peer0.org2.jwclab.com/msp:/etc/hyperledger/fabric/msp -v /home/mau/env-Monitoring/test-network/organizations/peerOrganizations/org2.jwclab.com/peers/peer0.org2.jwclab.com/tls:/etc/hyperledger/fabric/tls -v /home/mau/env-Monitoring/test-network/channel-artifacts/:/etc/hyperledger/fabric/channel-artifacts -v /home/mau/env-Monitoring/test-network/organizations/peerOrganizations/org2.jwclab.com/users/:/etc/hyperledger/fabric/users/ -v /home/mau/env-Monitoring/chaincode:/etc/hyperledger/fabric/chaincode --name peer0.org2.jwclab.com --network jwcnetwork -w /etc/hyperledger/fabric/ -p 9051:9051 -itd hyperledger/fabric-peer:2.2.0 

docker network inspect jwcnetwork 

docker exec -ti peer0.org2.jwclab.com sh
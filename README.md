# Proof-of-Concept for IBM MQ


**MacOs specifics**
```shell
podman machine stop || true
podman machine rm || true
podman machine init --cpus=2 --memory=4096 -v $HOME:$HOME -v /private/tmp:/private/tmp -v /var/folders/:/var/folders/
sed -i '' 's/security_model=mapped-xattr/security_model=none/' $(podman machine inspect | jq --raw-output '.[0].ConfigPath.Path')
podman machine start
```

**Pulling an MQ image from IBM Container Registry**

`podman pull icr.io/ibm-messaging/mq:latest`

Preparing a volume for persisting queue data and starting a container:
```shell
podman volume create qm1data
podman run --env 'LICENSE=accept' --env 'MQ_QMGR_NAME=QM1' --volume qm1data:/mnt/mqm --publish 1414:1414 --publish 9443:9443 --detach --env MQ_APP_PASSWORD=mqpass --env MQ_ADMIN_PASSWORD=mqpass --name ibmmq icr.io/ibm-messaging/mq:latest
podman cp ./config ibmmq:/tmp/config
```

**Console access**

https://localhost:9443/ibmmq/console/#/ (admin/mqpass)

**Setting up the IBM MQ topics**
```shell
podman exec -it ibmmq runmqsc QM1 -f /tmp/config/setup-queues.mq
```

**Stopping and cleaning**
```shell
podman rm -f ibmmq
podman volume rm qm1data 
```

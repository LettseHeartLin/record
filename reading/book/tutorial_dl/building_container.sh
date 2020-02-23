 
docker run  -p 2379:22 --name=dev-build-gpu -it -w /tensorflow -v /home/yzh/mypro:/home/yzh/mypro -e HOST_PERMS="$(id -u):$(id -g)"  192.168.20.118:5000/build-tensorflow-cpu     /bin/bash


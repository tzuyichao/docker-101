
docker image build -t helloworld-build -f Dockerfile.build .

docker container create --name helloworld-build-container helloworld-build

docker container cp helloworld-build-container:/myapp/helloworld .

docker image build -t helloworld .

docker container rm -f helloworld-build-container

Remove-Item helloworld

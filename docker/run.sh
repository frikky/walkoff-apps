# Verifies if vm.max_map_count is set or not for elasticsearch 
if [ $(/sbin/sysctl -b vm.max_map_count) -lt 262144 ]; then
	echo "[!] sysctl vm.max_map_count is less than 262144 - minimum requirement for elastic. Command:\n"
	echo "$ sysctl -w vm.max_map_count=262144"
	exit
fi

# Save all required images 
## echo "Saving worker"
## docker save localhost:5000/worker:latest -o ./images/worker.tar
## echo "Saving umpire"
## docker save localhost:5000/umpire:latest -o ./images/umpire.tar
## echo "Saving api_gateway"
## docker save localhost:5000/api_gateway:latest -o ./images/api_gateway.tar
## echo "Saving postgres"
## docker save postgres -o ./images/postgres.tar
## echo "Saving registry"
## docker save registry:2 -o ./images/registry.tar
## echo "Saving redis"
## docker save redis:latest -o ./images/redis.tar

echo "Creating the docker network"
docker network create walkoff_default

echo "Running postgres"
docker stop postgres 
docker rm postgres 
docker rmi postgres 

docker load -i ./images/postgres.tar

docker run \
	--network walkoff_default\
	-e TZ=Europe/Oslo \
	--env-file postgres.env \
	-p 5432:5432 \
	-h postgres \
	--name postgres \
	--restart always \
	-d postgres 


echo "Loading and running redis"
docker stop redis 
docker rm redis 
docker rmi redis

docker load -i ./images/redis.tar

docker run \
	--network walkoff_default\
	-e TZ=Europe/Oslo \
	-p 6379:6379 \
	-h redis \
	--name redis \
	--restart always \
	-d redis

echo "Loading and running registry"
docker stop registry
docker rm registry
docker rmi registry:2 

docker load -i ./images/registry.tar

docker run \
	--network walkoff_default\
	--volume $(pwd)/data/registry:/var/lib/registry \
	-e TZ=Europe/Oslo \
	-h registry \
	--name registry \
	--restart always \
	-d registry:2

echo "Loading and running api gateway"
docker stop walkoff_api_gateway_1
docker rm walkoff_api_gateway_1
docker rmi localhost:5000/api_gateway:latest

docker load -i ./images/api_gateway.tar

docker run \
	--network walkoff_default\
	-e TZ=Europe/Oslo \
	-p 8080:8080 \
	--env-file api_gateway.env \
	-h api_gateway \
	--name api_gateway \
	--restart always \
	-d localhost:5000/api_gateway:latest


# FIXME - can't connect to docker and control docker manager properly yet
echo "Loading and running umpire"
# Remove them all
docker stop umpire 
docker rm umpire 
docker rmi localhost:5000/umpire:latest --force

docker load -i ./images/umpire.tar

docker run \
	--network walkoff_default\
	--volume /var/run/docker.sock:/var/run/docker.sock:rw \
	--volume $(pwd)/apps:/app/apps \
	-e TZ=Europe/Oslo \
	--env-file umpire.env \
	-h umpire \
	--name umpire \
	--restart always \
	-d localhost:5000/umpire:latest
#

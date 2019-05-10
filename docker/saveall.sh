# Save all required images 
mkdir images
echo "Saving worker"
docker save localhost:5000/worker:latest -o ./images/worker.tar
echo "Saving umpire"
docker save localhost:5000/umpire:latest -o ./images/umpire.tar
echo "Saving api_gateway"
docker save localhost:5000/api_gateway:latest -o ./images/api_gateway.tar
echo "Saving postgres"
docker save postgres -o ./images/postgres.tar
echo "Saving registry"
docker save registry:2 -o ./images/registry.tar
echo "Saving redis"
docker save redis:latest -o ./images/redis.tar
echo "Saving walkoff_app_sdk"
docker save localhost:5000/walkoff_app_sdk -o ./images/walkoff_app_sdk.tar

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi localhost:5000/api_gateway:latest 
docker rmi localhost:5000/walkoff_app_sdk:latest
docker rmi localhost:5000/worker:latest
docker rmi worker:latest
docker rmi localhost:5000/umpire:latest
docker rmi walkoff_app_sdk:latest
docker rmi walkoff_app_hello_world:latest
docker rmi walkoff_app_nsa_search:latest
docker rmi walkoff_app_thehive:latest
docker rmi localhost:5000/walkoff_app_thehive:0.0.3 
docker rmi localhost:5000/walkoff_app_nsa_search:0.0.1
docker rmi localhost:5000/walkoff_app_hello_world:1.0.0 

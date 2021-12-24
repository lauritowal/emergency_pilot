# Build image
`docker build --no-cache --tag laurito-guidance -f DockerfileWind .`

# Run container
`docker run -d -v ~/ray_results:/root/ray_results -p 9999:6006 laurito-guidance`

# Delete image 
`docker rmi laurito-guidance`


# Log ouput of container
`docker logs -f <CONTAINER_ID>`

# Other stuff
## List content of image without starting container
```
docker create --name laurito-guidance laurito-guidance:latest
docker export laurito-guidance | tar t > laurito-guidance.txt
```

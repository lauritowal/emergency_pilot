# Build image
`docker build --no-cache --tag laurito-sincos-no-wind .`

# Run container
`docker run -d laurito-sincos-no-wind`

# Delete image 
`docker rmi laurito-sincos-no-wind`

# Log ouput of container
`docker logs -f <CONTAINER_ID>`

# Other stuff
## List content of image without starting container
```
docker create --name laurito-sincos-no-wind-v0 laurito-sincos-no-wind-v0:latest
docker export laurito-sincos-no-wind-v0 | tar t > laurito-sincos-no-wind-v0.txt
```
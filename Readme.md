# Build image
`docker build --no-cache --tag laurito-sincos-no-wind .`

# Run container
`docker run laurito-sincos-no-wind`

# Delete image 
`docker rmi laurito-sincos-no-wind`

# Other stuff
## List content of image without starting container
```
docker create --name laurito-sincos-no-wind-v0 laurito-sincos-no-wind-v0:latest
docker export laurito-sincos-no-wind-v0 | tar t > laurito-sincos-no-wind-v0.txt
```
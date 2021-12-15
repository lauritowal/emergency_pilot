# Build image
`   `

# Run container
`docker run -d -v ~/ray_results:/root/ray_results -p 9999:6006 laurito-guidance-sincos-no-wind`

# Delete image 
`docker rmi laurito-guidance-sincos-no-wind`


# Log ouput of container
`docker logs -f <CONTAINER_ID>`

# Other stuff
## List content of image without starting container
```
docker create --name laurito-guidance-sincos-no-wind laurito-guidance-sincos-no-wind:latest
docker export laurito-guidance-sincos-no-wind | tar t > laurito-guidance-sincos-no-wind.txt
```
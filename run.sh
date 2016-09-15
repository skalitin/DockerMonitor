docker run -d \
    --restart=on-failure \
    --name=dockermonitor \
    -p 8090:8080 \
    -v $(pwd)/src:/src \
    rmaz/dockermonitor


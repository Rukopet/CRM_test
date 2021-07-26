#!/bin/bash

docker build -t domclick .
docker run -p 80:80 -p 5000:5000 -it domclick
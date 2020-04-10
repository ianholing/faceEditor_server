#!/bin/bash
docker build -t faceeditor .
docker run --name=faceEditor -d -it --restart=always -p 5001:5001 -v $PWD:/faceEditor faceeditor


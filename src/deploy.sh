#!/usr/bin/env bash
docker stop h2txt_app || true && docker rm h2txt_app || true
docker image rm h2txt
docker build -f Dockerfile -t h2txt .
docker run -d -it -p 5000:5000 --name h2txt_app h2txt
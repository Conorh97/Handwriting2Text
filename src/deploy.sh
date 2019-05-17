#!/usr/bin/env bash
cd frontend
docker stop h2txt_frontend || true && docker rm h2txt_frontend || true
docker image rm ember
docker build -f Dockerfile -t ember .
docker run -d -it --network host --name h2txt_frontend ember

cd backend
sudo pip3 install -r req.txt
bash run.sh
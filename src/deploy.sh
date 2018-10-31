#!/usr/bin/env bash
docker stop h2txt_app || true && docker rm h2txt_app || true
docker build -t h2txt .
docker run -dp 5000:5000 --name h2txt_app h2txt
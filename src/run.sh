#!/usr/bin/env bash
rm -rf backend/static/*
cd frontend
ember serve
cd ../backend/
FLASK_APP=app.py python3 -m flask run --host=0.0.0.0 --port=5000
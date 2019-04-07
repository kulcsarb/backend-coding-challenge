#!/usr/bin/env bash
cd frontend && ./build.sh && cd ..
cp frontend/build/* backend/static/
sudo docker build -t translator/backend -f backend/Dockerfile ./backend

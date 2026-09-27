# Habit Tracker

A small Flask + SQLite web app for tracking daily habits and streaks, containerized with Docker.

## Run it

```bash
docker build -t habit-tracker .
docker run -p 5000:5000 habit-tracker
```

Then open http://localhost:5000

## Stop it

```bash
docker ps                  # find the container ID or name
docker stop <container_id>
```

## Useful commands

```bash
docker images                     # list images on your machine
docker ps -a                      # list all containers (running + stopped)
docker logs <container_id>        # view container output/logs
docker exec -it <container_id> sh # open a shell inside the running container
docker rm <container_id>          # remove a stopped container
docker rmi habit-tracker          # remove the image
```

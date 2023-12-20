docker volume create chech_volume



docker build -t stop_extremizm_bot .
docker run -d --restart unless-stopped -v chech_volume:/usr/src/app/data stop_extremizm_bot

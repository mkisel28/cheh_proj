docker volume create chech_volume
docker run -v chech_volume:/usr/src/app/data -d your_image_name
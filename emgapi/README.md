# emg-examples


docker build --rm -t emg/scipy-notebook .

docker run --rm -p 8888:8888 -v $(pwd)/examples:/home/jovyan/work emg/scipy-notebook start-notebook.sh

# emg-examples

### Run in docker

    docker build --rm -t emg/scipy-notebook .

    docker run --rm -p 8888:8888 -v $(pwd)/examples:/home/jovyan/work emg/scipy-notebook start-notebook.sh


### Run in conda

Download anaconda from https://www.anaconda.com/download/

    wget https://repo.continuum.io/archive/Anaconda3-5.0.0-Linux-x86_64.sh
    bash Anaconda3-5.0.0-Linux-x86_64.sh -b -p /path/to/anaconda3
    export PATH=/path/to/anaconda3/bin:$PATH

    pip install jsonapi-client

### Run in virtualenv

    virtualenv /path/to/venv
    source /path/to/venv/bin/activate

    pip install pandas numpy scipy jsonapi-client

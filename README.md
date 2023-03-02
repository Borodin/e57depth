# e57depth
This repository contains a script for converting e57 files to tiff files

## Run
```bash
python3 main.py --input_path=./input --output_path=./output
```
```bash
-h, --help
-i INPUT_PATH, --input_path=INPUT_PATH
-o OUTPUT_PATH, --output_path=OUTPUT_PATH
```

## Docker
Install [Docker](https://www.docker.com/) and run the following command:
```bash
docker run --rm -v "$(pwd)/input:/input" -v "$(pwd)/output:/output" ghcr.io/borodin/e57depth:master
```
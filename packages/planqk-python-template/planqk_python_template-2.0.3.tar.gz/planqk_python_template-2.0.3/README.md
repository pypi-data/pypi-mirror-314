# planqk-python-template

## Development

### Setup

```bash
conda env create -f environment.yml
conda activate planqk-python-template
```

### Run tests

```bash
pytest
```

### Run it locally

```bash
python3 -m src
```

## Run with Docker

### Build the parent image

```bash
docker build -t registry.gitlab.com/planqk-foss/planqk-python-template .
```

### Build the service image

```bash
cd user_code
zip -r ../user_code.zip .
cd ..

docker build --build-arg USER_CODE_FILE=user_code.zip -t planqk-service --file dockerfile-template/Dockerfile .
```

### Run the service image

Run the `planqk-service` as follows:

```bash
docker run -it planqk-service
```

## License

Apache-2.0 | Copyright 2023-2024 Kipu Quantum GmbH

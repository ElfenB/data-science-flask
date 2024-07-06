# data-science-flask

This project hosts a Flask application that calculates salaries based on various factors.

The model was trained in a separate Jupyter notebook using the dataset from [tidytuesday](https://github.com/rfordatascience/tidytuesday/blob/master/data/2021/2021-05-18/readme.md).

This is not about the data preparation or the model training but just hosts a shiny frontend to interact with the finished model.

## Demo

Link to the hosted application: [https://data-science.benelfen.com](https://data-science.benelfen.com)

## Installation

Install data-science-flask

If wanted, [Taskfile](https://taskfile.dev) can be used.

A specific Python version is needed to interact with the model. Also, the specific versions of numpy and scikit are required. For that, the [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) should be used.

```bash
# Create new venv
python -m venv .venv

# Install packages
pip install -r requirements.txt

# Start application with Taskfile (binary is included in repository)
./task start

# Alternatively, start with Python directly
python app.py
```

## Deployment

To deploy this project run

```bash
docker compose up --build -d
```

## Authors

- [@ElfenB](https://www.github.com/ElfenB)

## License

[MIT](https://choosealicense.com/licenses/mit/)

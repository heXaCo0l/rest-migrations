# Rest Migrations

Rest Migrations is a Python package designed to refresh Django migrations folders. It simplifies the process of cleaning up migrations folders by removing all files except the `__init__.py` file.

## Installation
To install Rest Migrations, you can follow these steps:

1- Clone the repository from GitHub using the following command:
```sh
git clone https://github.com/heXaCo0l/rest-migrations.git
```
2- Navigate to the cloned repository:
```sh
cd rest-migrations
```

3- Install the package using pip:
```sh
pip install .
```

## Usage:
```py
from rest_migrations.main import ProjectRunner
ProjectRunner.run()
```

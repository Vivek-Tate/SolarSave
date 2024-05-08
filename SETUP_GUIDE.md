# Setup Guide

## STEP 1 - Install pip

```bash
python -m pip install --upgrade pip
```

## STEP 2 - Install virtualenv
(to isolate the versioning of the dependencies so they don't clash with global variables)

```bash
python -m pip install --user virtualenv
```

## STEP 3 - Create a Virtual Environment

```bash
python -m venv .venv
```

## STEP 4 - Activate the Virtual Environment

```bash
.venv/Scripts/Activate
# FOR MAC:
.venv/bin/activate
```

## STEP 5 - Install Dependencies

```bash
# Ensure that you are in the project root directory
# (directory containing the README file)
python -m pip install .
python -m pip install -r tests/requirements.txt
```

## STEP 6 - Initialize the Database

```bash
# To initialise and EMPTY database
python -m flask --app solar_offset init-db

# To populate the database with the given test data
python -m flask --app solar_offset init-db .\tests\data.sql

# You can select another sql file to populate the database with different data
# For guidance on the database tables and columns, see the `solar_offset/schema.sql` file
```

## STEP 7 - Run the Web Application Development Server

```bash
python -m flask --app solar_offset run -h localhost --port 8000
```

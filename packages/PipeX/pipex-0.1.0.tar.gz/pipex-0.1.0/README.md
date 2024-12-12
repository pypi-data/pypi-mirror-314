# **PipeX**

PipeX is a CLI-based tool for managing and automating end-to-end ETL (Extract, Transform, Load) workflows. It simplifies data pipeline tasks such as extracting data from APIs and databases, transforming data with custom logic, and loading it into storage solutions like AWS S3 or databases.

## **Features**

- Extract data from APIs, CSV/JSON files, and relational databases (MySQL, PostgreSQL).
- Transform data using custom Python scripts powered by Pandas.
- Load transformed data into target systems like AWS S3 or other databases.
- Real-time logging and monitoring.
- Scalable scheduling with Kubernetes CronJobs.

---

<!-- add a highlight suggesting that right now extracting through api and loading to s3 works, everything else is still in progress -->

> **Note:** Currently, extracting data through APIs and loading it to AWS S3 is fully functional. Other features are still in progress.

## **Installation**

### **Prerequisites**

1. Python 3.11 or higher.
2. Poetry for dependency management. Install Poetry:
   ```bash
   pip install poetry
   ```

### **Setup**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pipex.git
   cd pipex
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

4. Install PipeX globally to use as a CLI:
   ```bash
   poetry build
   pip install dist/pipex-0.1.0-py3-none-any.whl
   ```

---

## **Usage**

### **Running the CLI**

To start the CLI, use the command:

```bash
pipex
```

### **Available Commands**

```bash
pipex --help
```

This will display all available commands and their usage.

#### Example Commands:

1. **Extract Data**  
   Extract data from a MySQL database:

   ```bash
   pipex extract db --host localhost --user root --password secret --db mydb --query "SELECT * FROM table_name"
   ```

2. **Transform Data**  
   Apply transformations to a CSV file:

   ```bash
   pipex transform --input data.csv --script transform_script.py --output transformed_data.csv
   ```

3. **Load Data**  
   Load transformed data to an S3 bucket:

   ```bash
   pipex load s3 --file transformed_data.csv --bucket my-bucket --key data/transformed_data.csv
   ```

4. **Run Full Pipeline**  
   Run the entire ETL process in one command:
   ```bash
   pipex run --config pipeline_config.yaml
   ```

---

## **Configuration**

PipeX uses YAML configuration files to define ETL workflows. Example:

```yaml
extract:
  type: db
  host: localhost
  user: root
  password: secret
  db: mydb
  query: "SELECT * FROM table_name"

transform:
  script: transform_script.py

load:
  type: s3
  bucket: my-bucket
  key: data/transformed_data.csv
```

Save this configuration as `pipeline_config.yaml` and run:

```bash
pipex run --config pipeline_config.yaml
```

---

## **Environment Variables**

PipeX uses a `.env` file to manage sensitive information like API keys and database credentials. Follow these steps to set up your `.env` file:

1. **Create a `.env` File**: Copy the `.env.example` file to `.env` and fill in your credentials.

```sh
cp .env.example .env
```

2. **Edit the `.env` File**: Open the `.env` file and fill in your AWS credentials and API details.

```properties
# .env

# AWS Credentials
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=your-region
BUCKET_NAME=your-bucket-name

# API Credentials
API_TOKEN=your-api-token
API_ENDPOINT=your-api-endpoint
```

---

## **Development**

### **File Structure**

```plaintext
PipeX/
├── app/
│   ├── api.py
│   ├── cli.py
│   ├── extract.py
│   ├── load.py
│   ├── storage.py
│   ├── transform.py
│   ├── utils.py
│   └── __init__.py
├── config/
│   ├── settings.py
│   ├── logging_config.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   ├── test_load.py
│   └── test_cli.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── README.md
```

---

## **Contributing**

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes and push:
   ```bash
   git push origin feature/new-feature
   ```
4. Submit a pull request.

---

## **License**

This project is licensed under the MIT License.

---

## **Author**

Developed by [Agnivesh Kumar](mailto:agniveshkumar15@gmail.com).

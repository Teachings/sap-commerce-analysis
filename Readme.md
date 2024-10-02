# SAP Commerce Properties Comparison App Wiki

This document provides instructions on how to run the **SAP Commerce Properties Comparison App** both locally using Python and Conda, and as a Docker container. Additionally, it explains the purpose of the three main endpoints exposed by the app.

---

## 1. **Running the App Locally with Conda Environment**

### Prerequisites

- Ensure that you have **Conda** installed.
- Ensure **Python 3.11** is installed.

### Steps

1. **Create a Conda environment**:

   Open your terminal and run the following command to create a new Conda environment:

   ```bash
   conda create --name sap-commerce-env python=3.11
   ```

2. **Activate the Conda environment**:

   After creating the environment, activate it:

   ```bash
   conda activate sap-commerce-env
   ```

3. **Install required dependencies**:

   Ensure you have a `requirements.txt` file with the following content:

   Install the dependencies in the Conda environment:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI app**:

   Use Uvicorn to run the FastAPI app locally:

   ```bash
   uvicorn app.main:app --reload
   ```

   This will start the app at `http://127.0.0.1:8000` by default.

---

## 2. **Running the App in Docker on a Custom Port**

Ensure **Docker** is installed and running.

1. **Build the Docker image**:

   In the directory where your `Dockerfile` and application files are located, build the Docker image:

   ```bash
   docker build -t sap-commerce-analysis .
   ```

2. **Run the Docker container on a custom port**:

   To run the container on a specific port, such as `8006`, use the following command:

   ```bash
   docker run -d -p 8006:8000 --name sap-commerce-analysis sap-commerce-analysis
   ```

   This maps the container’s internal port `8000` to your local port `8006`. You can now access the app at `http://localhost:8006`.

---

## 3. **Available Endpoints**

The FastAPI app exposes three main endpoints, each serving a specific purpose:

### 3.1. **Homepage for Properties File Comparison**

- **Endpoint**: `GET /`
- **Purpose**: This is the default homepage that allows users to compare two properties files by uploading them. It is designed to help you identify the differences, common properties, and missing keys between the files.
- **Usage**: Navigate to the homepage to start comparing properties files.

### 3.2. **Logs Analysis Page**

- **Endpoint**: `GET /logs`
- **Purpose**: This page is designed to analyze and display logs that you upload. You can upload logs and filter them based on specific criteria, like logger names or other patterns, for easier troubleshooting.
- **Usage**: Access this page to analyze log files and filter out important information based on the logger names or errors.

### 3.3. **Static JavaScript File for HAC Properties Extraction**

- **Endpoint**: `GET /script`
- **Purpose**: This serves a static JavaScript file which is used for extracting SAP Commerce HAC properties. To use this, go to the SAP Commerce Platform's configuration page, show all properties, open the browser’s developer console, and run this JavaScript file. The script will generate a JSON file containing all the properties, which you can later use for properties file comparison.
- **Usage**: Access the script at this endpoint, copy its contents, and run it in the dev console on the SAP Commerce HAC configuration page.

---

## Additional Notes

- **Logs and Debugging**: To view the logs for the FastAPI app when running locally, you can inspect the terminal where the app is running. If using Docker, you can view logs using:

  ```bash
  docker logs <container_id>
  ```

- **Contributing**: If you'd like to contribute to the project, ensure that you have the app running locally, and test any changes thoroughly. PRs are welcome.

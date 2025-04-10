# Fantasy Football Analytics Platform

A personal data engineering project that processes Fantasy Premier League (FPL) data, analyzes it, and deploys it to the cloud.

## Features
- Data collection via the official FPL API
- Data processing with PySpark (coming soon)
- Visualization with Streamlit (planned)
- Deployment to AWS using Terraform (optional)

## Project Structure

├── data/ # Raw and processed data 
├── src/
│ ├── data_ingestion/ # API interfaces, data ingestion
│ ├── etl/ # Transformations with PySpark 
│ └── utils/ # Utility functions 
├── terraform/ # Infrastructure-as-Code setup for S3, Glue, etc. 
└── dashboard/ # Frontend (e.g., Streamlit)

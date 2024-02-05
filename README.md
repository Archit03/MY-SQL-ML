# Machine Learning and Database Interaction Project

## Overview

This project combines database interaction and machine learning to analyze query logs and predict outcomes using a given MySQL database. Additionally, a machine learning model is trained on a Querylog.csv dataset for classification purposes.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)

## Setup

### Requirements

- Python (>=3.6)
- MySQL Server
- Libraries: pandas, scikit-learn, matplotlib, seaborn, imbalanced-learn, mysql-connector-python

### Installation

1. Download the repository:

   ```bash
   cd ~/MY-SQL-ML-main 
   pip install -r requirements.txt
   python -m venv cuda # Create a virtual environment
   # For cuda environment please download cuda from https://developer.nvidia.com/cuda-toolkit and install it
   .\cuda\Scripts\activate 
   ```
### Usage
1. Create a MYSQL database into your local RDMS.
   ```bash
   python InsertMYSQL.py #This will inject all SQL statements into the DB. 
   ```
2. Generate random queries 
   ```bash
   python Generate_Quereies.py # To generate ramdom SELECT, INSERT, UPDATE, DELETE queries.
   ```
3. Create a query log of the executed queries. 
   ```bash 
    python Query_log.py #This will create two .csv log file of the execu
   ```
4. Run the ML mode 
   ```Bash
    Python ML.py  #This will create a model and save it as "predicted_outcomes.csv" file.
   ```
   

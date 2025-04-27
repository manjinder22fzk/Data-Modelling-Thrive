# Consolidated Conversations Data Pipeline

## 🚀 Solution 1 Overview

This is the first solution, following the given instructions closely without introducing significant changes or experiments.  
However, to bring a real-world production touch, I enhanced it by building an automated pipeline that handles the entire setup process — including:

- Creating a virtual environment
- Installing all required Python dependencies
- Setting up the necessary directory structure
- Executing the ETL pipeline end-to-end

In actual industry-level projects, automation is critical for efficiency, scalability, and error reduction.  
Thus, this solution mimics how problems are solved professionally in production environments.

If you would like to run the entire pipeline seamlessly, simply clone the repository onto your local system and execute:

```bash
bash run_pipeline.sh


## 📚 Project Overview

This project consolidates user conversations from three source tables (`users`, `conversation_start`, and `conversation_parts`) into a unified format.  
The goal is to build a **fact table** (`consolidated_messages`) tracking all conversation messages, supported by **dimension tables** for users and conversation metadata.

The project follows a modular real-world ETL flow:
- **Schema Creation → Data Loading → Serving Layer**
- **Python and SQL modular scripts**
- **Logging, error handling, and audit readiness**

---

## ⚙️ Tech Stack

| Component     | Technology    |
| :------------ | :-------------|
| Language      | Python 3.10+   |
| Database      | SQLite3        |
| ETL Scripts   | SQL Modular Scripts |
| Orchestration | Python (`load_consolidated_messages.py`) + Shell (`run_pipeline.sh`) |
| Logging       | Python Logging |
| Data Export   | Pandas CSV Export |

---

## 🏗️ Project Structure

```
conversation_pipeline/
├── README.md
├── requirements.txt
├── run_pipeline.sh
├── database/
│   └── thrive_test_db.db
├── scripts/
│   ├── create_consolidated_messages_table.sql
│   ├── load_consolidated_messages.sql
├── src/
│   └── load_consolidated_messages.py
├── output/
│   └── consolidated_messages.csv
├── logs/
│   └── app.log
```

---

## 🚀 How to Run the Pipeline - 

### Just run the following command in git bash terminal.

```
bash run_pipeline.sh  
```


The pipeline will:
- Connect to the SQLite database
- Create the database schema
- Load and consolidate data
- Export the final `consolidated_messages.csv`
- Save logs in the `logs/` directory

---

## 🛠️ Pipeline Key Steps

- Drops any existing tables and recreates schema on each run.
- Loads users and conversation parts into dimension tables.
- Loads conversation starters and conversation parts into the `consolidated_messages` fact table.
- Handles cases where the conversation starter is not the customer.
- Sorts the final messages by `conversation_id` and `created_at`.
- Exports the final data to a CSV file.

---

## 📈 Data Model Summary

| Table                   | Type         | Purpose                                           |
| :----------------------- | :----------- | :------------------------------------------------ |
| `users`                  | Source Table | Original user information                         |
| `conversation_start`     | Source Table | Conversation starting messages                    |
| `conversation_parts`     | Source Table | Additional conversation messages (comments, closes, etc.) |
| `dim_users`              | Dimension    | Enriched user information for reporting           |
| `dim_conversation_parts` | Dimension    | Metadata for conversation parts                   |
| `consolidated_messages`  | Fact Table    | Unified conversation thread with customers        |

---
## 🧠 Potential Improvements for Production Systems

---

### 1. Normalize `message_type` into a Dimension Table

Currently, `message_type` is stored as free text like `'open'`, `'comment'`, etc.

**Recommendation:** Create a `dim_message_types` table to enforce controlled vocabulary and improve query performance.

```sql
CREATE TABLE dim_message_types (
    message_type_id INTEGER PRIMARY KEY,
    message_type_text TEXT UNIQUE
);
```

---

### 2. Add Indexes for Query Performance

For large datasets, create indexes on frequently queried columns:

```sql
CREATE INDEX idx_conversation_id ON consolidated_messages (conversation_id);
CREATE INDEX idx_created_at ON consolidated_messages (created_at);
```

Benefits:
- Faster retrieval by conversation
- Better performance for sorting and filtering

---

### 3. Use Database Views Instead of Materialized Tables

Instead of materializing `consolidated_messages`, create a dynamic database view:

```sql
CREATE VIEW vw_consolidated_messages AS
WITH conversation_starts_cte AS (...),
conversation_parts_cte AS (...)
SELECT * FROM (
    SELECT * FROM conversation_starts_cte
    UNION ALL
    SELECT * FROM conversation_parts_cte
)
ORDER BY conversation_id, created_at;
```

Benefits:
- Always reflects the latest data
- No need for periodic ETL runs

---

### 4. Introduce Mini Change Data Capture (CDC)

Instead of full reloads, track incremental changes:

```sql
SELECT * FROM conversation_parts WHERE created_at > last_successful_etl_time;
```

Benefits:
- Faster ETL runs
- Reduced system load
- Supports near-real-time updates

---

### 5. Partition the Fact Table for Scalability

If `consolidated_messages` grows massively, partition it by month or conversation_id buckets.

Example:

```sql
CREATE TABLE consolidated_messages_2025_04 AS
SELECT * FROM consolidated_messages
WHERE strftime('%Y-%m', created_at, 'unixepoch') = '2025-04';
```

Benefits:
- Faster queries
- Optimized table scans

---

### 6. Implement Retry Mechanisms for Critical Steps

Add retry logic for steps like:

- Connecting to database
- Writing outputs

Example (Python):

```python
import time

for attempt in range(3):
    try:
        conn = sqlite3.connect(DB_PATH)
        break
    except Exception:
        time.sleep(2 ** attempt)
```

Benefits:
- Increased pipeline robustness
- Handles transient errors gracefully

---



### 7. Config Driven Architecture

Move hardcoded paths into `config.py` or `.env` files.

Example `config.py`:

```python
DB_PATH = "database/thrive_test_db.db"
OUTPUT_PATH = "output/consolidated_messages.csv"
```

Benefits:
- Easy to switch between dev/stage/prod
- Cleaner code

---


### 8. Add Alerting on ETL Failures

Integrate email or Slack alerts when a job fails.

Example (Python concept):

```python
import smtplib
# send email if exception occurs
```

Benefits:
- Immediate visibility into issues
- Faster recovery time

---

### 9. Dockerize the Pipeline

Wrap everything inside a Docker container.

Example Dockerfile:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["bash", "run_pipeline.sh"]
```

Benefits:
- Easy deployment across environments
- Isolation from system dependencies

---

### 10. Add Unit Tests for Core Functions

Use `pytest` to write unit tests for:

- Database connection
- SQL script execution
- CSV export

Benefits:
- Higher code reliability
- Easier maintenance

---



---

## 📢 Assumptions

- All conversations and parts are linked to valid users.
- `created_at` fields use UNIX epoch integer format.
- Source data is assumed clean and consistently populated.

---

## 📚 Credits

Built using best practices in:

- Scalable Data Engineering
- Dimensional Modeling (Star Schema)
- Production-ready ETL Design
# Consolidated Conversations Data Pipeline

## 📚 Project Overview

This project consolidates user conversations from three source tables (`users`, `conversation_start`, and `conversation_parts`) into a unified format.  
The goal is to build a **fact table** (`consolidated_messages`) tracking all conversation messages, supported by **dimension tables** for users and conversation metadata.

The project follows a modular real-world ETL flow:
- **Schema Creation → Data Loading → Serving Layer**
- **Python and SQL modular scripts**
- **Logging, error handling, and audit readiness**

---

## ⚙️ Tech Stack

| Component     | Technology    |
| :------------ | :-------------|
| Language      | Python 3.10+   |
| Database      | SQLite3        |
| ETL Scripts   | SQL Modular Scripts |
| Orchestration | Python (`load_consolidated_messages.py`) + Shell (`run_pipeline.sh`) |
| Logging       | Python Logging |
| Data Export   | Pandas CSV Export |

---

## 🏗️ Project Structure

```
conversation_pipeline/
├── README.md
├── requirements.txt
├── run_pipeline.sh
├── database/
│   └── thrive_test_db.db
├── scripts/
│   ├── create_consolidated_messages_table.sql
│   ├── load_consolidated_messages.sql
├── src/
│   └── load_consolidated_messages.py
├── output/
│   └── consolidated_messages.csv
├── logs/
│   └── app.log
```

---

## 🚀 How to Run the Pipeline

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Run the ETL pipeline:

```bash
bash run_pipeline.sh
```

The pipeline will:
- Connect to the SQLite database
- Create the database schema
- Load and consolidate data
- Export the final `consolidated_messages.csv`
- Save logs in the `logs/` directory

---

## 🛠️ Pipeline Key Steps

- Drops any existing tables and recreates schema on each run.
- Loads users and conversation parts into dimension tables.
- Loads conversation starters and conversation parts into the `consolidated_messages` fact table.
- Handles cases where the conversation starter is not the customer.
- Sorts the final messages by `conversation_id` and `created_at`.
- Exports the final data to a CSV file.

---

## 📈 Data Model Summary

| Table                   | Type         | Purpose                                           |
| :----------------------- | :----------- | :------------------------------------------------ |
| `users`                  | Source Table | Original user information                         |
| `conversation_start`     | Source Table | Conversation starting messages                    |
| `conversation_parts`     | Source Table | Additional conversation messages (comments, closes, etc.) |
| `dim_users`              | Dimension    | Enriched user information for reporting           |
| `dim_conversation_parts` | Dimension    | Metadata for conversation parts                   |
| `consolidated_messages`  | Fact Table    | Unified conversation thread with customers        |

---

## 🧠 Potential Improvements for Production Systems

### 1. Normalize `message_type` into a Dimension Table

Currently, `message_type` is stored as free text like 'open', 'comment', etc.

**Recommendation:** Create a `dim_message_types` table to enforce controlled vocabulary and improve query performance.

```sql
CREATE TABLE dim_message_types (
    message_type_id INTEGER PRIMARY KEY,
    message_type_text TEXT UNIQUE
);
```

---

### 2. Add Indexes for Query Performance

For large datasets, create indexes on frequently queried columns:

```sql
CREATE INDEX idx_conversation_id ON consolidated_messages (conversation_id);
CREATE INDEX idx_created_at ON consolidated_messages (created_at);
```

Benefits:
- Faster retrieval by conversation
- Better performance for sorting and filtering

---

### 3. Use Database Views Instead of Materialized Tables

For real-time latest data without reloading:

```sql
CREATE VIEW vw_consolidated_messages AS
WITH conversation_starts_cte AS (...),
conversation_parts_cte AS (...)
SELECT * FROM (
    SELECT * FROM conversation_starts_cte
    UNION ALL
    SELECT * FROM conversation_parts_cte
)
ORDER BY conversation_id, created_at;
```

Benefits:
- No periodic ETL required
- Always reflects current state of source tables

---

### 4. Introduce Mini Change Data Capture (CDC)

Instead of full reloads on every ETL, fetch only new or updated records:

```sql
SELECT * FROM conversation_parts WHERE created_at > last_successful_etl_time;
```

Benefits:
- Faster incremental loads
- Reduces system load

---

### 5. Future Scalability: Partitioning the Fact Table

If the `consolidated_messages` table becomes very large, partition it:

```sql
CREATE TABLE consolidated_messages_2025_04 AS
SELECT * FROM consolidated_messages
WHERE strftime('%Y-%m', created_at, 'unixepoch') = '2025-04';
```

Benefits:
- Reduces query scan time
- Improves performance for monthly reporting

---

## 📢 Assumptions

- All conversations and parts are linked to valid users.
- `created_at` fields use UNIX epoch integer format.
- Source data is assumed clean and consistently populated.

---

## 📚 Credits

Built using best practices in:

- Scalable Data Engineering
- Dimensional Modeling (Star Schema)
- Production-ready ETL Design

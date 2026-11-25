# Milestone 16: Database Schema & ER Diagram

## 1. Entity-Relationship Overview
The SQLite database stores raw datasets, column definitions, individual records, augmented samples, validation outcomes, and training experiment benchmarks.

```mermaid
erDiagram
    DATASETS ||--o{ DATASET_RECORDS : contains
    DATASETS ||--o{ AUGMENTED_RECORDS : produces
    DATASETS ||--o{ TRAINING_EXPERIMENTS : evaluates
    TRAINING_EXPERIMENTS ||--o{ MODEL_METRICS : records

    DATASETS {
        int id PK
        string name
        string modality
        string task_type
        int row_count
        int column_count
        string input_column
        string target_column
        string id_column
        json preserved_columns
        json columns_metadata
        datetime created_at
    }

    DATASET_RECORDS {
        int id PK
        int dataset_id FK
        json data_json
        datetime created_at
    }

    AUGMENTED_RECORDS {
        int id PK
        int dataset_id FK
        string algorithm
        json original_row_json
        json augmented_row_json
        boolean is_valid
        float validation_score
        string rejection_reason
        datetime created_at
    }

    TRAINING_EXPERIMENTS {
        int id PK
        int dataset_id FK
        string model_name
        string task_type
        float test_size
        int random_state
        float baseline_accuracy
        float augmented_accuracy
        float baseline_macro_f1
        float augmented_macro_f1
        json baseline_metrics_json
        json augmented_metrics_json
        datetime created_at
    }

    MODEL_METRICS {
        int id PK
        int experiment_id FK
        string metric_name
        float baseline_value
        float augmented_value
        float delta
    }
```

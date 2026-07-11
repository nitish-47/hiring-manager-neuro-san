# init_db.py
import sqlite3

def init_mock_database():
    # Connects to a local file database (creates it if it doesn't exist)
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    # Create the candidate pool table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_pool (
        id TEXT PRIMARY KEY,
        experience TEXT NOT NULL,
        skills TEXT NOT NULL
    );
    """)

    # Mock technical data matching advanced infrastructure/data engineering requirements
    mock_candidates = [
        (
            "jane",
            "5 years of experience building distributed backend systems. Specialized in moving high-throughput event data streams and handling enterprise state clusters.",
            "Python,TypeScript,Apache Kafka,Kubernetes,Docker,FastAPI"
        ),
        (
            "doe",
            "Senior Data Infrastructure specialist with 6+ years migrating massive relational tables over to cloud distributed processing nodes. High proficiency with ETL optimizations.",
            "Python,SQL,Azure Databricks,Apache Spark,PySpark,Delta Lake"
        ),
        (
            "nitish",
            "Frontend React developer with 3 years engineering interactive dashboards, single page interfaces, and complex state management trees.",
            "TypeScript,React,NextJS,TailwindCSS,Redux"
        )
    ]

    # Insert data safely bypassing duplicate primary keys if run multiple times
    cursor.executemany("""
    INSERT OR REPLACE INTO candidate_pool (id, experience, skills)
    VALUES (?, ?, ?);
    """, mock_candidates)

    conn.commit()
    
    # Verify records were inserted successfully
    cursor.execute("SELECT COUNT(*) FROM candidate_pool;")
    count = cursor.fetchone()[0]
    conn.close()

    print(f" Success: Mock SQLite database initialized with {count} candidate records.")

if __name__ == "__main__":
    init_mock_database()
"""
generate_data.py

Generates realistic mock candidate records (name-based id, experience,
skills, email) and loads them into candidates.db, matching the schema
in init_db.py.

Uses Faker for names/emails, and a randomized template engine for the
"experience" free-text field so descriptions read naturally instead of
looking copy-pasted.
"""

import argparse
import random
import sqlite3

from faker import Faker

fake = Faker()

# ---------------------------------------------------------------------------
# Role archetypes: each has a skill pool, a seniority-appropriate title pool,
# and sentence fragments used to build a natural-sounding experience blurb.
# Mixing and matching these at random gives a lot of combinatorial variety
# without needing an external LLM call.
# ---------------------------------------------------------------------------
ROLE_ARCHETYPES = [
    {
        "name": "Backend / Distributed Systems",
        "titles": ["Backend Engineer", "Distributed Systems Engineer", "Platform Engineer"],
        "skills": ["Python", "Go", "TypeScript", "Apache Kafka", "Kubernetes",
                   "Docker", "FastAPI", "gRPC", "Redis", "PostgreSQL"],
        "focus_phrases": [
            "building distributed backend systems",
            "designing high-throughput event-driven services",
            "operating large-scale microservice architectures",
            "engineering fault-tolerant streaming pipelines",
        ],
        "detail_phrases": [
            "Specialized in moving high-throughput event data streams and handling enterprise state clusters.",
            "Focused on reducing p99 latency across service meshes serving millions of requests daily.",
            "Deep experience with container orchestration and zero-downtime deployment strategies.",
            "Built internal tooling for observability, tracing, and incident response at scale.",
        ],
    },
    {
        "name": "Data Infrastructure / ETL",
        "titles": ["Data Infrastructure Engineer", "Data Platform Engineer", "Analytics Engineer"],
        "skills": ["Python", "SQL", "Azure Databricks", "Apache Spark", "PySpark",
                   "Delta Lake", "Airflow", "Snowflake", "dbt", "AWS Glue"],
        "focus_phrases": [
            "migrating massive relational tables to cloud distributed processing nodes",
            "designing warehouse-scale ETL/ELT pipelines",
            "optimizing large batch and streaming data workflows",
            "building lakehouse architectures for analytics teams",
        ],
        "detail_phrases": [
            "High proficiency with ETL optimizations and cost-aware query tuning.",
            "Led data quality and lineage initiatives across multiple business units.",
            "Experienced in partitioning strategy design for petabyte-scale datasets.",
            "Built self-service data pipelines used by dozens of downstream analytics teams.",
        ],
    },
    {
        "name": "Frontend",
        "titles": ["Frontend Engineer", "UI Engineer", "Product Engineer"],
        "skills": ["TypeScript", "React", "NextJS", "TailwindCSS", "Redux",
                   "GraphQL", "Vite", "Storybook", "Jest", "Playwright"],
        "focus_phrases": [
            "engineering interactive dashboards and single-page interfaces",
            "building design systems and component libraries",
            "developing complex state management trees",
            "shipping performant, accessible customer-facing web apps",
        ],
        "detail_phrases": [
            "Strong focus on component reusability and design-system consistency.",
            "Experienced in performance profiling and reducing bundle sizes for large SPAs.",
            "Collaborated closely with design teams to implement pixel-accurate UI.",
            "Built end-to-end test suites to keep release velocity high without regressions.",
        ],
    },
    {
        "name": "ML / Applied AI",
        "titles": ["Machine Learning Engineer", "Applied AI Engineer", "ML Platform Engineer"],
        "skills": ["Python", "PyTorch", "TensorFlow", "scikit-learn", "MLflow",
                   "Kubernetes", "Ray", "Airflow", "SQL", "Docker"],
        "focus_phrases": [
            "building and deploying production ML pipelines",
            "fine-tuning and serving large language models",
            "designing feature stores and model-serving infrastructure",
            "developing recommendation and ranking systems",
        ],
        "detail_phrases": [
            "Experienced in taking models from notebook prototypes to production-grade services.",
            "Built monitoring for model drift, data drift, and inference latency.",
            "Worked on distributed training jobs across multi-GPU clusters.",
            "Collaborated with research teams to productionize experimental models.",
        ],
    },
    {
        "name": "DevOps / SRE",
        "titles": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Infrastructure Engineer"],
        "skills": ["Terraform", "AWS", "Kubernetes", "Docker", "Prometheus",
                   "Grafana", "Python", "Ansible", "GitHub Actions", "Helm"],
        "focus_phrases": [
            "operating and scaling cloud infrastructure",
            "building CI/CD pipelines and infrastructure-as-code",
            "improving system reliability and on-call response",
            "hardening production environments for security and uptime",
        ],
        "detail_phrases": [
            "Reduced deployment times significantly through automated CI/CD pipelines.",
            "Owned incident response process, improving MTTR across core services.",
            "Implemented infrastructure-as-code standards adopted company-wide.",
            "Built self-healing infrastructure using autoscaling and health-check automation.",
        ],
    },
]


def make_id(name: str, used_ids: set) -> str:
    """Turn a Faker name into a lowercase, unique, DB-friendly id."""
    base = name.split()[0].lower()  # first name, like the sample data ("jane", "doe")
    candidate = base
    suffix = 1
    while candidate in used_ids:
        suffix += 1
        candidate = f"{base}{suffix}"
    used_ids.add(candidate)
    return candidate


def make_experience(archetype: dict, years: int) -> str:
    title = random.choice(archetype["titles"])
    focus = random.choice(archetype["focus_phrases"])
    detail = random.choice(archetype["detail_phrases"])
    plus = "+" if random.random() < 0.4 else ""
    opener_templates = [
        f"{years}{plus} years of experience {focus}.",
        f"{title} with {years}{plus} years {focus}.",
        f"{years}-year track record {focus} as a {title}.",
    ]
    opener = random.choice(opener_templates)
    return f"{opener} {detail}"


def make_skills(archetype: dict, min_skills=4, max_skills=6) -> str:
    k = random.randint(min_skills, min(max_skills, len(archetype["skills"])))
    chosen = random.sample(archetype["skills"], k=k)
    return ",".join(chosen)


def generate_candidates(n: int):
    used_ids = set()
    candidates = []
    for _ in range(n):
        name = fake.name()
        archetype = random.choice(ROLE_ARCHETYPES)
        years = random.randint(2, 12)

        cand_id = make_id(name, used_ids)
        experience = make_experience(archetype, years)
        skills = make_skills(archetype)
        email = fake.email()

        candidates.append((cand_id, experience, skills, email))
    return candidates


def load_into_db(candidates, db_path="candidates.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_pool (
        id TEXT PRIMARY KEY,
        experience TEXT NOT NULL,
        skills TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)

    # NOTE: original script's INSERT omitted the `email` column, which would
    # violate the NOT NULL constraint. Fixed here to include all 4 columns.
    cursor.executemany("""
    INSERT OR REPLACE INTO candidate_pool (id, experience, skills, email)
    VALUES (?, ?, ?, ?);
    """, candidates)

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM candidate_pool;")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def main():
    parser = argparse.ArgumentParser(description="Generate mock candidate data.")
    parser.add_argument("-n", "--num", type=int, default=20,
                         help="Number of candidate records to generate (default: 20)")
    parser.add_argument("--db", type=str, default="candidates.db",
                         help="Path to the SQLite database file")
    parser.add_argument("--seed", type=int, default=None,
                         help="Random seed for reproducible generation")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        Faker.seed(args.seed)

    candidates = generate_candidates(args.num)
    count = load_into_db(candidates, db_path=args.db)

    print(f"Success: {args.db} initialized/updated with {count} candidate records.")
    print("\nSample of generated records:")
    for row in candidates[:5]:
        print(f"  id={row[0]:<15} email={row[3]:<30} skills={row[2]}")


if __name__ == "__main__":
    main()
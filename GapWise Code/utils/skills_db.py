"""
utils/skills_db.py

Single source of truth for the skill vocabulary used by BOTH resume
parsing and job-description parsing.

Previously resume/skill_extractor.py and job/job_description.py each
kept their own short, slightly different SKILL_DATABASE, which meant a
skill could be detected in the JD but never in the resume (or vice
versa) and show up as a false "gap".

Two structures are exported:

  SKILL_ALIASES   {alias -> canonical skill}
                  Handles the many ways one skill gets written:
                  "sklearn"/"scikit learn" -> "Scikit-Learn",
                  "js" -> "JavaScript", "k8s" -> "Kubernetes".

  SKILL_DATABASE  set of every searchable surface form (canonical
                  names + all aliases), lowercased.

Add new skills to SKILL_GROUPS below - everything else derives from it.
"""


# ------------------------------------------------------------------
# Canonical skill -> list of alternate spellings / abbreviations
# Grouped by domain purely for readability.
# ------------------------------------------------------------------

SKILL_GROUPS = {

    # ----------------------------------------------------------
    "Programming Languages": {
        "Python": ["python3", "py"],
        "Java": [],
        "C": [],
        "C++": ["cpp", "c plus plus"],
        "C#": ["c sharp", "csharp", "dotnet", ".net"],
        "JavaScript": ["js", "ecmascript", "es6"],
        "TypeScript": ["ts"],
        "Go": ["golang"],
        "Rust": [],
        "Ruby": [],
        "PHP": [],
        "Swift": [],
        "Kotlin": [],
        "Scala": [],
        "R": [],
        "MATLAB": [],
        "Perl": [],
        "Dart": [],
        "Objective-C": ["objective c"],
        "Shell Scripting": ["bash", "shell", "zsh", "shell script"],
        "PowerShell": [],
        "VBA": ["visual basic"],
        "Assembly": [],
        "Julia": [],
        "Haskell": [],
        "Groovy": [],
        "Solidity": [],
    },

    # ----------------------------------------------------------
    "Web Frontend": {
        "HTML": ["html5"],
        "CSS": ["css3"],
        "React": ["reactjs", "react.js"],
        "Angular": ["angularjs"],
        "Vue": ["vuejs", "vue.js"],
        "Svelte": ["sveltekit"],
        "Next.js": ["nextjs", "next js"],
        "Nuxt.js": ["nuxtjs", "nuxt"],
        "jQuery": [],
        "Bootstrap": [],
        "Tailwind CSS": ["tailwind", "tailwindcss"],
        "Material UI": ["mui", "material-ui"],
        "Sass": ["scss"],
        "Redux": [],
        "Webpack": [],
        "Vite": [],
        "Responsive Design": ["responsive web design"],
        "Web Accessibility": ["a11y", "wcag"],
    },

    # ----------------------------------------------------------
    "Web Backend": {
        "Node.js": ["nodejs", "node js", "node"],
        "Express": ["expressjs", "express.js"],
        "Django": [],
        "Flask": [],
        "FastAPI": ["fast api"],
        "Spring Boot": ["spring", "springboot"],
        "Laravel": [],
        "Ruby on Rails": ["rails", "ror"],
        "ASP.NET": ["asp net", "aspnet"],
        "NestJS": ["nest js"],
        "Streamlit": [],
        "Gradio": [],
        "REST API": ["rest", "restful", "rest apis", "restful api"],
        "GraphQL": [],
        "gRPC": [],
        "WebSockets": ["websocket"],
        "Microservices": ["microservice architecture"],
        "API Design": ["api development"],
        "OAuth": ["oauth2", "oauth 2.0"],
        "JWT": ["json web token"],
    },

    # ----------------------------------------------------------
    "Databases": {
        "SQL": [],
        "MySQL": [],
        "PostgreSQL": ["postgres"],
        "SQLite": [],
        "MongoDB": ["mongo"],
        "Redis": [],
        "Cassandra": [],
        "Oracle": ["oracle db", "oracle database"],
        "Microsoft SQL Server": ["sql server", "mssql", "t-sql", "tsql"],
        "DynamoDB": [],
        "Elasticsearch": ["elastic search"],
        "Neo4j": ["graph database"],
        "Firebase": ["firestore"],
        "Supabase": [],
        "Snowflake": [],
        "BigQuery": ["google bigquery"],
        "Redshift": ["amazon redshift"],
        "Database Design": ["schema design", "data modeling", "data modelling"],
        "Query Optimization": ["sql tuning"],
        "PL/SQL": ["plsql"],
    },

    # ----------------------------------------------------------
    "Data Science & Analytics": {
        "NumPy": ["numpy"],
        "Pandas": [],
        "Matplotlib": [],
        "Seaborn": [],
        "Plotly": [],
        "SciPy": [],
        "Statsmodels": [],
        "Data Analytics": ["data analysis", "analytics"],
        "Data Science": [],
        "Data Visualization": ["data visualisation", "dataviz"],
        "Statistics": ["statistical analysis"],
        "Probability": [],
        "Hypothesis Testing": ["a/b testing", "ab testing"],
        "Exploratory Data Analysis": ["eda"],
        "Feature Engineering": [],
        "Time Series Analysis": ["time series", "forecasting"],
        "Power BI": ["powerbi"],
        "Tableau": [],
        "Looker": ["looker studio"],
        "Excel": ["microsoft excel", "ms excel", "advanced excel"],
        "Google Sheets": ["spreadsheets"],
        "Data Cleaning": ["data wrangling", "data preprocessing"],
        "Data Mining": [],
    },

    # ----------------------------------------------------------
    "Machine Learning & AI": {
        "Machine Learning": ["ml"],
        "Deep Learning": ["dl"],
        "Scikit-Learn": ["sklearn", "scikit learn", "scikitlearn"],
        "TensorFlow": ["tensor flow"],
        "Keras": [],
        "PyTorch": ["torch"],
        "XGBoost": [],
        "LightGBM": [],
        "CatBoost": [],
        "Hugging Face": ["huggingface", "transformers library"],
        "NLP": ["natural language processing"],
        "Computer Vision": ["cv", "image processing"],
        "OpenCV": ["open cv"],
        "Generative AI": ["gen ai", "genai"],
        "LLM": ["llms", "large language model", "large language models"],
        "LangChain": ["lang chain"],
        "LlamaIndex": ["llama index"],
        "RAG": ["retrieval augmented generation", "retrieval-augmented generation"],
        "Prompt Engineering": [],
        "Agentic AI": ["ai agents", "autonomous agents"],
        "Vector Databases": ["vector db", "pinecone", "chroma", "chromadb", "faiss", "weaviate", "qdrant"],
        "Reinforcement Learning": ["rl"],
        "Neural Networks": ["ann", "artificial neural network"],
        "CNN": ["convolutional neural network"],
        "RNN": ["recurrent neural network", "lstm", "gru"],
        "Transformers": ["transformer architecture", "attention mechanism"],
        "Model Deployment": ["ml deployment", "model serving"],
        "MLOps": ["ml ops"],
        "MLflow": ["ml flow"],
        "Model Evaluation": ["model validation", "cross validation"],
        "Hyperparameter Tuning": ["hyperparameter optimization", "grid search"],
        "Recommendation Systems": ["recommender systems", "recommendation engine"],
        "Anomaly Detection": ["outlier detection"],
        "Clustering": ["kmeans", "k-means"],
        "Classification": [],
        "Regression": ["linear regression", "logistic regression"],
        "Speech Recognition": ["asr", "speech to text"],
        "OCR": ["optical character recognition", "tesseract"],
        "Explainable AI": ["xai", "shap", "lime"],
        "Responsible AI": ["ai ethics", "ai safety"],
    },

    # ----------------------------------------------------------
    "Big Data & Engineering": {
        "Apache Spark": ["spark", "pyspark"],
        "Hadoop": ["hdfs", "mapreduce"],
        "Apache Kafka": ["kafka"],
        "Apache Airflow": ["airflow"],
        "Hive": ["apache hive"],
        "Databricks": [],
        "ETL": ["etl pipelines", "elt"],
        "Data Engineering": [],
        "Data Warehousing": ["data warehouse"],
        "Data Pipelines": ["pipeline development"],
        "dbt": ["data build tool"],
        "Apache Flink": ["flink"],
        "Data Lake": ["datalake"],
    },

    # ----------------------------------------------------------
    "Cloud & DevOps": {
        "AWS": ["amazon web services", "ec2", "s3", "lambda"],
        "Azure": ["microsoft azure"],
        "GCP": ["google cloud", "google cloud platform"],
        "Docker": ["containerization", "containerisation"],
        "Kubernetes": ["k8s"],
        "Jenkins": [],
        "CI/CD": ["ci cd", "continuous integration", "continuous deployment"],
        "Terraform": ["infrastructure as code", "iac"],
        "Ansible": [],
        "GitHub Actions": ["gh actions"],
        "GitLab CI": ["gitlab ci/cd"],
        "Linux": ["unix"],
        "Nginx": [],
        "Apache": ["apache http server"],
        "Serverless": ["serverless architecture"],
        "Cloud Architecture": ["cloud computing"],
        "Monitoring": ["prometheus", "grafana", "observability"],
        "Load Balancing": [],
        "Heroku": [],
        "Vercel": [],
        "Netlify": [],
    },

    # ----------------------------------------------------------
    "Tools & Version Control": {
        "Git": [],
        "GitHub": [],
        "GitLab": [],
        "Bitbucket": [],
        "Jira": [],
        "Confluence": [],
        "Postman": [],
        "VS Code": ["visual studio code"],
        "Jupyter": ["jupyter notebook", "jupyter lab"],
        "Google Colab": ["colab"],
        "Figma": [],
        "Notion": [],
        "Slack": [],
        "Trello": [],
        "Anaconda": ["conda"],
        "Maven": [],
        "Gradle": [],
    },

    # ----------------------------------------------------------
    "Mobile": {
        "Android Development": ["android"],
        "iOS Development": ["ios"],
        "React Native": [],
        "Flutter": [],
        "Xamarin": [],
        "Mobile App Development": ["mobile development"],
    },

    # ----------------------------------------------------------
    "Testing & Quality": {
        "Unit Testing": ["unit tests"],
        "Integration Testing": [],
        "PyTest": ["pytest"],
        "JUnit": [],
        "Selenium": [],
        "Cypress": [],
        "Jest": [],
        "Test Automation": ["automated testing", "qa automation"],
        "Manual Testing": [],
        "Test Driven Development": ["tdd"],
        "Debugging": [],
        "Code Review": [],
    },

    # ----------------------------------------------------------
    "Security": {
        "Cybersecurity": ["cyber security", "information security", "infosec"],
        "Penetration Testing": ["pen testing", "ethical hacking"],
        "Network Security": [],
        "Cryptography": ["encryption"],
        "Application Security": ["appsec"],
        "Vulnerability Assessment": [],
        "SIEM": [],
        "Firewall": [],
    },

    # ----------------------------------------------------------
    "Computer Science Fundamentals": {
        "Data Structures": ["data structure"],
        "Algorithms": ["algorithm design", "dsa"],
        "Object Oriented Programming": ["oop", "object-oriented programming"],
        "Operating Systems": ["os"],
        "Computer Networks": ["networking", "tcp/ip"],
        "System Design": ["distributed systems", "scalability"],
        "Design Patterns": [],
        "Compiler Design": [],
        "Problem Solving": ["analytical skills"],
        "Competitive Programming": [],
    },

    # ----------------------------------------------------------
    "Business & Domain": {
        "Agile": ["agile methodology"],
        "Scrum": [],
        "Kanban": [],
        "Project Management": [],
        "Product Management": [],
        "Business Analysis": ["business analyst"],
        "Requirement Gathering": ["requirements analysis"],
        "Stakeholder Management": [],
        "Digital Marketing": ["seo", "sem"],
        "Financial Analysis": ["finance"],
        "Supply Chain": ["logistics"],
        "Healthcare Analytics": [],
        "Risk Management": [],
    },

    # ----------------------------------------------------------
    "Soft Skills": {
        "Communication": ["communication skills", "verbal communication"],
        "Teamwork": ["collaboration", "team player"],
        "Leadership": ["team leadership"],
        "Critical Thinking": [],
        "Time Management": [],
        "Adaptability": ["flexibility"],
        "Presentation Skills": ["public speaking"],
        "Documentation": ["technical writing"],
        "Mentoring": ["coaching"],
        "Customer Service": ["client handling"],
    },
}


# ------------------------------------------------------------------
# Derived lookups
# ------------------------------------------------------------------

def _build():

    aliases = {}

    for group in SKILL_GROUPS.values():

        if not isinstance(group, dict):
            continue

        for canonical, alts in group.items():

            if not isinstance(canonical, str):
                continue

            aliases[canonical.lower()] = canonical

            for alt in (alts or []):
                aliases[alt.lower()] = canonical

    return aliases


SKILL_ALIASES = _build()

# Every searchable surface form (canonical + aliases), lowercased.
SKILL_DATABASE = set(SKILL_ALIASES.keys())


def canonical_skill(text):
    """
    Maps any recognised spelling to its canonical display name.
    Returns None if the text isn't a known skill.
    """

    if not text:
        return None

    return SKILL_ALIASES.get(text.strip().lower())


def all_canonical_skills():
    """Sorted list of every canonical skill name."""

    return sorted(set(SKILL_ALIASES.values()))

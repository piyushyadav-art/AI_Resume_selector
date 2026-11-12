SKILL_RECOMMENDATIONS = {
    # Programming & Frameworks
    "python":
        "Learn Python fundamentals, OOP, data structures, type hinting, and standard libraries.",
    "java":
        "Learn Core Java, OOP principles, Collections Framework, concurrency, and Spring Boot.",
    "c++":
        "Master C++ fundamentals, STL containers, pointers, memory management, and modern C++ (C++17/20).",
    "c#":
        "Learn C# syntax, .NET Core / .NET 8, LINQ, async/await patterns, and ASP.NET APIs.",
    "javascript":
        "Master modern ES6+ JavaScript, asynchronous programming (Promises/async-await), DOM, and closures.",
    "typescript":
        "Learn TypeScript type systems, interfaces, generics, and strict type safety for large scale applications.",
    "html":
        "Study semantic HTML5, accessibility (a11y), forms, SEO best practices, and document structure.",
    "css":
        "Master modern CSS (Flexbox, CSS Grid, responsive design, animations, and CSS variables).",
    "react":
        "Learn React hooks, state management (Context/Redux/Zustand), component lifecycle, and Next.js.",
    "node.js":
        "Learn Node.js asynchronous event-driven runtime, Express/Fastify frameworks, middleware, and REST architecture.",
    "fastapi":
        "Learn FastAPI, Pydantic data validation, async route handlers, dependency injection, and OpenAPI documentation.",
    "flask":
        "Study Flask routing, blueprints, templates (Jinja2), extensions (SQLAlchemy/Flask-Login), and deployment.",
    "django":
        "Learn Django MVT architecture, ORM, authentication, Django REST Framework (DRF), and admin configuration.",
    "web development":
        "Build full-stack web applications integrating frontend UI with backend APIs and databases.",

    # Databases & Cloud / DevOps
    "sql":
        "Learn SQL queries, multi-table joins, subqueries, indexing, constraints, and relational database design.",
    "mysql":
        "Master MySQL server administration, query optimization, indexing strategies, and replication.",
    "postgresql":
        "Learn PostgreSQL advanced features: JSONB, window functions, CTEs, full-text search, and performance tuning.",
    "mongodb":
        "Learn NoSQL document modeling, MongoDB aggregation pipelines, indexing, and Mongoose ORM.",
    "docker":
        "Learn Docker containers, writing optimized multi-stage Dockerfiles, Docker Compose, and volume networking.",
    "kubernetes":
        "Study Kubernetes architecture, Pods, Deployments, Services, Ingress, ConfigMaps, and Helm charts.",
    "aws":
        "Learn AWS core services: EC2, S3, Lambda, RDS, IAM, ECS/EKS, and CloudWatch.",
    "azure":
        "Learn Microsoft Azure fundamentals: Azure App Services, Azure Blob Storage, Azure Functions, and Entra ID.",
    "git":
        "Learn Git version control: branching strategies, merging, rebasing, resolving merge conflicts, and git hooks.",
    "github":
        "Master GitHub workflows: Pull Requests, GitHub Actions (CI/CD pipelines), issue tracking, and repository security.",

    # AI, Data Science & Machine Learning
    "numpy":
        "Learn NumPy array operations, vectorization, broadcasting, linear algebra, and mathematical operations.",
    "pandas":
        "Master Pandas DataFrames, data cleaning, filtering, grouping, aggregation, merging, and time-series analysis.",
    "matplotlib":
        "Practice data visualization with Matplotlib and Seaborn (histograms, scatter plots, subplots, and heatmaps).",
    "scikit-learn":
        "Learn classical ML algorithms (classification, regression, clustering), cross-validation, pipelines, and evaluation metrics.",
    "machine learning":
        "Study supervised learning, unsupervised learning, feature engineering, overfitting mitigation, and model evaluation.",
    "deep learning":
        "Learn deep neural networks, activation functions, backpropagation, CNNs, RNNs, and optimization algorithms.",
    "pytorch":
        "Learn PyTorch tensors, autograd, nn.Module architectures, custom datasets/dataloaders, and training loops.",
    "tensorflow":
        "Learn TensorFlow 2.x, Keras functional API, model callbacks, training pipelines, and TensorBoard.",
    "nlp":
        "Learn text processing, tokenization, embeddings (Word2Vec/BERT), sentiment analysis, and LLM text generation.",
    "natural language processing":
        "Study transformer architectures, attention mechanisms, fine-tuning Hugging Face models, and tokenization.",
    "computer vision":
        "Study OpenCV, image preprocessing, object detection (YOLO), convolutional networks, and segmentation.",
    "langchain":
        "Learn LangChain abstractions: Prompts, Output Parsers, LCEL, Retrieval-Augmented Generation (RAG), and Tools.",
    "langgraph":
        "Learn LangGraph cyclic graphs, state management, nodes, edges, conditional routing, and multi-agent systems.",
    "data analysis":
        "Practice exploratory data analysis (EDA), hypothesis testing, statistical modeling, and insights reporting.",

    # Mechanical, Maintenance & Industrial Operations
    "centrifugal pumps":
        "Study pump mechanics, impeller types, head calculations, alignment, mechanical seals, and cavitation prevention.",
    "preventive maintenance":
        "Learn PM scheduling, lubrication routes, equipment inspection checklists, and condition monitoring.",
    "routine greasing":
        "Learn lubricant selection, bearing lubrication intervals, grease gun operation, and contamination prevention.",
    "filter cleaning":
        "Learn strainer and filter inspection, cleaning procedures, differential pressure monitoring, and mesh replacement.",
    "strainer filter cleaning":
        "Study inline strainer maintenance, basket cleaning protocols, differential pressure checks, and seal integrity.",
    "lube oil filling":
        "Understand lube oil viscosity grades, contamination testing, topping-off procedures, and oil level sight glass checks.",
    "troubleshooting":
        "Practice root cause analysis (RCA), vibration analysis, thermal imaging, and systematic equipment diagnostics.",
    "oil and gas":
        "Learn upstream/downstream processes, plant safety protocols (OSHA/HSE), process flow diagrams (PFDs), and P&IDs.",
    "logbook management":
        "Master standard operating logbooks, shift handover documentation, parameter recording, and maintenance logs.",
    "equipment maintenance":
        "Study mechanical equipment upkeep, wear-and-tear inspection, teardown procedures, and replacement schedules.",
    "plant operations":
        "Learn industrial plant workflows, process control, safety shutdown systems (ESD), and utility management.",
    "pumps":
        "Understand positive displacement vs dynamic pumps, priming, flow rate regulation, and mechanical seals.",
    "valves":
        "Study gate, globe, ball, butterfly, check, and pressure relief valves, actuation, and packing maintenance.",
    "compressors":
        "Learn reciprocating and rotary screw compressors, compression stages, lubrication, and pressure relief systems.",
    "hydraulic systems":
        "Understand hydraulic circuits, hydraulic fluids, cylinders, directional control valves, and pressure regulation.",
    "pneumatic systems":
        "Study compressed air distribution, FRL units (Filter-Regulator-Lubricator), actuators, and pneumatic valves.",

    # Soft Skills & Management
    "team collaboration":
        "Engage in collaborative cross-functional projects, code reviews, agile standups, and shared documentation.",
    "problem solving":
        "Practice algorithmic problem solving, structured debugging, and systematic root cause analysis.",
    "project management":
        "Learn Agile/Scrum methodologies, sprint planning, Kanban boards, and milestone tracking.",
    "innovative thinking":
        "Explore novel architectures, prototype innovative proof-of-concepts, and stay updated with emerging AI research."
}


def recommend_skills(missing_skills):
    """
    Generates tailored learning recommendations for missing skills.
    """
    recommendations = {}
    for skill in missing_skills:
        skill_clean = skill.strip().lower()
        if skill_clean in SKILL_RECOMMENDATIONS:
            recommendations[skill] = SKILL_RECOMMENDATIONS[skill_clean]
        else:
            recommendations[skill] = (
                f"Learn the fundamentals of {skill.title()}. "
                "Practice with hands-on projects and apply it to real-world problem scenarios."
            )
    return recommendations
# Intelligent Candidate Discovery & Ranking System

AI-powered candidate ranking system built for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**.

The system goes beyond simple keyword matching and combines:

* Semantic Job Description Matching
* Candidate Profile Understanding
* Career History Analysis
* Production AI Experience Detection
* Behavioral Signal Analysis
* Honeypot / Fake Match Detection
* Multi-factor Hybrid Ranking

to identify candidates that genuinely fit the role.

---

# Project Overview

Traditional ATS systems rank candidates using keyword matching.

This project uses a hybrid ranking approach:

```text
Job Description
       │
       ▼
JD Parser
       │
       ▼
Candidate Processing
       │
       ▼
Feature Engineering
       │
       ▼
Rule-Based Scoring
       │
       ▼
Top-K Candidate Selection
       │
       ▼
Semantic Re-ranking
       │
       ▼
Final Ranking
       │
       ▼
Submission CSV
```

The system understands:

* What the JD actually means
* Production experience
* AI/ML maturity
* Retrieval/Search expertise
* Ranking system knowledge
* Behavioral hiring signals

instead of blindly matching keywords.

---

# Architecture

## Stage 1: JD Understanding

File:

```text
src/jd_parser.py
```

Responsibilities:

* Reads job description
* Extracts required capabilities
* Identifies:

  * Retrieval systems
  * Ranking systems
  * Embeddings
  * Vector databases
  * Python
  * ML experience
  * Evaluation frameworks

Output:

```python
{
    "required_keywords": [...]
}
```

---

## Stage 2: Candidate Pre-filtering

File:

```text
src/pre_filter.py
```

Purpose:

Reduce candidate pool before expensive processing.

Filters:

* Completely unrelated profiles
* Very low experience candidates
* Empty profiles
* Non-technical profiles

Example:

```text
100,000 candidates
      ↓
20,000 candidates
```

---

## Stage 3: Feature Engineering

File:

```text
src/feature_engineering.py
```

Extracts ranking signals.

Features include:

| Feature                   | Description                  |
| ------------------------- | ---------------------------- |
| experience_score          | Relevant experience          |
| retrieval_score           | Retrieval/Search expertise   |
| production_ml_score       | Production ML deployment     |
| evaluation_score          | Ranking evaluation knowledge |
| product_company_score     | Product company exposure     |
| python_score              | Python proficiency           |
| behavior_score            | Hiring intent                |
| market_demand_score       | Recruiter interest           |
| github_score              | Open-source activity         |
| external_validation_score | Public validation signals    |
| location_score            | Location compatibility       |
| semantic_score            | Semantic JD similarity       |

---

## Stage 4: Honeypot Detection

File:

```text
src/honeypot_detector.py
```

Detects misleading profiles.

Penalizes:

### Consulting-only careers

Examples:

```text
TCS
Infosys
Wipro
Cognizant
Accenture
Capgemini
Mindtree
```

### Pure Research Profiles

Examples:

```text
Research Labs
Academic-only work
Publication-only experience
```

### Framework Enthusiasts

Examples:

```text
LangChain only
Prompt engineering only
```

### CV-heavy Profiles

Examples:

```text
Computer Vision
GANs
Speech Recognition

without

NLP
Retrieval
Ranking
```

### Job Hoppers

Average tenure:

```text
< 18 months
```

---

## Stage 5: Rule-Based Ranking

File:

```text
src/candidate_scorer.py
```

Weighted scoring system.

Weights loaded from:

```text
config/weights.yaml
```

Example:

```yaml
experience_score: 0.10
semantic_score: 0.20
retrieval_score: 0.25
production_ml_score: 0.15
evaluation_score: 0.15
product_company_score: 0.10
python_score: 0.10
behavior_score: 0.05
```

Calculates:

```text
Candidate Fit Score
```

---

## Stage 6: Semantic Re-ranking

File:

```text
src/semantic_matcher.py
```

Uses:

```text
SentenceTransformer
```

Model:

```text
all-MiniLM-L6-v2
```

Process:

```text
Top 2000 Candidates
          ↓
Create Candidate Embeddings
          ↓
Create JD Embedding
          ↓
Cosine Similarity
          ↓
Semantic Score
          ↓
Re-rank Candidates
```

Benefits:

* Understands meaning
* Finds related skills
* Avoids keyword dependency

Example:

Candidate:

```text
Built recommendation system
```

JD:

```text
Search and ranking engineer
```

Keyword match:

```text
Low
```

Semantic match:

```text
High
```

---

## Stage 7: Reasoning Generation

File:

```text
src/reasoning_generator.py
```

Creates recruiter-friendly explanations.

Example:

```text
Senior Machine Learning Engineer with 7.2 yrs;
7 AI core skills (Weaviate, Recommendation Systems, Pinecone);
response rate 0.61
```

---

## Stage 8: Submission Generation

File:

```text
src/submission_builder.py
```

Produces:

```text
submission.csv
```

Format:

```csv
candidate_id,rank,score,reasoning
CAND_0018499,1,0.993,"Senior Machine Learning Engineer with 7.2 yrs; 7 AI core skills (Weaviate, Recommendation Systems, Pinecone); response rate 0.61"
```

---

# Input Format

## Candidate File

```text
data/candidates.jsonl
```

Each line:

```json
{
  "candidate_id": "CAND_000001",
  "profile": {},
  "career_history": [],
  "skills": [],
  "redrob_signals": {}
}
```

Dataset Size:

```text
100,000 candidates
```

---

## Job Description

```text
data/job_description.txt
```

Example:

```text
Senior AI Engineer
```

Contains:

* Requirements
* Preferred Skills
* Disqualifiers
* Hiring Signals

---

# Output Format

Generated file:

```text
outputs/submission.csv
```

Columns:

| Column       | Description           |
| ------------ | --------------------- |
| candidate_id | Candidate ID          |
| rank         | Candidate Rank        |
| score        | Normalized Score      |
| reasoning    | Recruiter Explanation |

Example:

```csv
candidate_id,rank,score,reasoning
CAND_0018499,1,0.993,"Senior Machine Learning Engineer with 7.2 yrs; 7 AI core skills (Weaviate, Recommendation Systems, Pinecone); response rate 0.61"
```

---

# Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Project

Run ranking:

```bash
python rank.py \
--candidates data/candidates.jsonl \
--jd data/job_description.txt \
--out outputs/submission.csv
```

Windows:

```bash
python rank.py --candidates data/candidates.jsonl --jd data/job_description.txt --out outputs/submission.csv
```

---

# Validate Submission

Run:

```bash
python validate_submission.py outputs/submission.csv
```

Expected:

```text
Validation successful.
```

---

# Performance Optimization

Current Strategy:

### Stage 1

Rule-Based Ranking

```text
100,000
    ↓
Top 2,000
```

### Stage 2

Semantic Re-ranking

```text
2,000
    ↓
Top 100
```

Benefits:

* Fast execution
* Low memory usage
* Better semantic relevance
* Fits hackathon time constraints

---

# Technologies Used

### Machine Learning

* Sentence Transformers
* Cosine Similarity

### NLP

* Semantic Matching
* Job Description Parsing

### Ranking

* Hybrid Scoring
* Weighted Ranking
* Semantic Re-ranking

### Python Libraries

```text
sentence-transformers
numpy
pandas
pyyaml
scikit-learn
tqdm
```

---

# Key Features

✅ Semantic JD Understanding

✅ Production ML Experience Detection

✅ Retrieval/Search Expertise Detection

✅ Ranking System Evaluation Knowledge

✅ Behavioral Hiring Signals

✅ Candidate Availability Analysis

✅ Honeypot Detection

✅ Hybrid Ranking System

✅ Recruiter-Friendly Reasoning

✅ Submission Validator Compatible


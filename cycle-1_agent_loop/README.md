# Cycle 1 — Self-Correcting SQL Agent

# 1. Problem Statement
Natural-language database queries may generate incorrect SQL queries due to invalid columns, syntax errors, or queries that return no results.

This project implements a self-correcting SQL agent that uses an LLM to generate SQL, executes it against a SQLite database, observes the result, and retries when required.

The agent follows:

**Perceive → Plan → Act → Observe**

# 2. Use Case
**UC3 — Self-Correcting SQL Agent**

The agent receives a natural-language database question and:

1. Generates SQL using Gemini.
2. Executes the SQL on the SQLite database.
3. Observes the result or error.
4. Corrects and retries when necessary.
5. Stops when a valid non-empty result is obtained or 5 iterations are completed.

# 3. Architecture
Architecture diagram:
`docs/architecture_diagram.drawio`

PNG version:
`docs/architecture_diagram.png`

# Flow

```text
User Request
     ↓
  Perceive
     ↓
    Plan
     ↓
 Gemini LLM
     ↓
     Act
     ↓
 SQLite Database
     ↓
   Observe
     ↓
 Success?
  ↙     ↘
Yes      No
 ↓        ↓
Stop   Retry
       (max 5)

# 4. Technology Stack

Language: Python
LLM: Google Gemini 2.5 Flash
LLM SDK: google-genai
Database: SQLite
Logging: JSON
Testing: pytest
Environment Management: python-dotenv

# 5. Agent Loop

Perceive
Receives the user's database question.

Plan
Gemini generates a SQLite SELECT query using the database schema and previous observation.

Act
The generated SQL is executed using the database tool.

Observe
The execution result or error is returned to the agent.

If the result is unsuccessful or empty, the agent retries with the previous observation.

# 6. Tools

The agent uses two callable tools:
get_database_schema()
execute_sql()

get_database_schema() retrieves the available tables and columns.
execute_sql() executes the generated SQL and returns the result or error.

# 7. Success Condition

The agent stops only when:
SQL execution succeeds
AND
at least one row is returned

Maximum iterations:
5
If the success condition is not achieved, the agent terminates after 5 iterations.

# 8. Failure Recovery

Example:
Iteration 1
SELECT name, score FROM students
        ↓
SQL Error: no such column: score
        ↓
Iteration 2
SELECT name, marks FROM students
        ↓
Successful Result

The agent recovers from the SQL failure without crashing.

# 9. Iteration Logging

Every iteration is stored in:
logs/agent_log.json

Each log records:
Iteration number
Planning summary
SQL action
Observation/result

# 10. Project Structure

cycle-1_agent_loop/
│
├── app/
│   ├── agent.py
│   ├── planner.py
│   └── tools.py
│
├── database/
│   └── database.py
│
├── logs/
│   └── agent_log.json
│
├── tests/
│
├── docs/
│   ├── architecture_diagram.drawio
│   └── architecture_diagram.png
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

# 11. Setup

Install dependencies
pip install -r requirements.txt
Configure API Key

Create a .env file:
GEMINI_API_KEY=your_api_key_here

# 12. Run

From the cycle-1_agent_loop directory:
python -u app/agent.py

Example input:
show me the names and marks of all students

Example output:
Generated SQL:
SELECT name, marks FROM students

Observation:
{'success': True, 'results': [...]}
Success condition met.

# 13. Testing

The agent was tested for:
   Successful SQL execution
   SQL failure and recovery
   Zero-result queries
   Maximum 5 iterations
   Iteration logging
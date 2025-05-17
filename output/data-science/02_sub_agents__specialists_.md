# Chapter 2: Sub-Agents (Specialists) - The Expert Team

Welcome back! In [Chapter 1: Root Agent (Orchestrator)](01_root_agent__orchestrator_.md), we met the "project manager" of our `data-science` system – the Root Agent. We learned that it understands your requests and delegates tasks. But who does it delegate to? That's where our **Sub-Agents**, or **Specialists**, come in!

Imagine our Root Agent is like the director of a movie. The director has the overall vision, but they rely on a team of experts: a cinematographer for camera work, a sound engineer for audio, actors for performing, and so on. Each specialist is an expert in their specific area.

Our Sub-Agents are just like that expert crew!

## Why Do We Need Specialists? The Power of Teamwork!

Let's think about our example from Chapter 1:

**"What were our total product sales last month, and can you show me if sales are generally going up or down?"**

This request has a few distinct parts:
1.  **Getting data:** "total product sales last month" – this needs database access.
2.  **Analyzing data:** "show me if sales are generally going up or down" – this needs calculation and interpretation.

It would be a lot to ask one single agent to be an expert in *everything* – talking to databases, performing complex statistical analysis, understanding machine learning, and more. It's much more effective to have a team of specialists.

**Sub-Agents are expert agents, each focused on a specific domain.**

*   One might be an expert at **querying databases** (like BigQuery).
*   Another might be a **data science whiz** (great at Python analysis).
*   Yet another could be a specialist in **managing machine learning models** (like BigQuery ML models).

Just like a real-world team with a database administrator, a data scientist, and an ML engineer, each sub-agent handles requests relevant to its expertise. This allows our system to tackle complex, multi-faceted problems efficiently and accurately.

## Meet the Team: Our Key Specialists

In our `data-science` project, we have a few key types of specialist sub-agents. Let's get to know them:

### 1. The Database Agent (BigQuery Specialist)

*   **Role:** The "Librarian" or "Database Guru."
*   **Expertise:** Talking to databases, especially Google BigQuery. Its main job is to fetch specific pieces of information.
*   **How it works:** When the Root Agent needs raw data (e.g., "sales figures for Q1," "list of customers in California"), it turns to the Database Agent. This agent is skilled at understanding what data is needed and (often with the help of [NL2SQL (Natural Language to SQL Conversion)](07_nl2sql__natural_language_to_sql_conversion_.md)) constructing the correct SQL query to retrieve it from BigQuery.

Let's look at a simplified version of how our `database_agent` is defined. You'll find the full code in `data_science/sub_agents/bigquery/agent.py`.

```python
# data_science/sub_agents/bigquery/agent.py (Simplified)
from google.adk.agents import Agent
from .prompts import return_instructions_bigquery # Agent's specific rules
from . import tools # Tools like running SQL queries

database_agent = Agent(
    name="database_agent",
    instruction=return_instructions_bigquery(), # Tells it how to handle database tasks
    tools=[
        tools.initial_bq_nl2sql, # A tool to help convert natural language to SQL
        tools.run_bigquery_validation # A tool to run and check SQL queries
    ],
    # ... other settings like which AI model to use
)
```
In this snippet:
*   `Agent(...)` creates our specialist.
*   `name="database_agent"` gives it a clear identifier.
*   `instruction=return_instructions_bigquery()`: This provides the Database Agent with its own set of "rules" or [Agent Prompts (Instructions)](03_agent_prompts__instructions_.md), tailored for database tasks.
*   `tools=[...]`: This lists the special [Tools (Capabilities)](04_tools__capabilities_.md) this agent can use. For instance, `initial_bq_nl2sql` helps turn your plain English question into a database query, and `run_bigquery_validation` actually runs that query on BigQuery.

So, if the Root Agent asks, "Get me last month's sales," the Database Agent uses its instructions and tools to figure out the right BigQuery query, run it, and return the sales data.

### 2. The Analytics Agent (Python Data Scientist)

*   **Role:** The "Data Cruncher" or "Insight Finder."
*   **Expertise:** Performing data analysis using Python. This agent can calculate statistics, identify trends, and sometimes even help visualize data.
*   **How it works:** Once the Root Agent has some raw data (perhaps from the Database Agent), it might pass it to the Analytics Agent for deeper analysis. For example, "Here's the sales data for the last year. Can you tell me the average monthly sales and if there's an upward trend?" The Analytics Agent uses its Python skills to perform these calculations.

Here's a peek at its simplified definition from `data_science/sub_agents/analytics/agent.py`:

```python
# data_science/sub_agents/analytics/agent.py (Simplified)
from google.adk.agents import Agent
from google.adk.code_executors import VertexAiCodeExecutor # For running Python
from .prompts import return_instructions_ds # Agent's specific rules

# This 'root_agent' is specific to the analytics sub-agent's own setup
root_agent = Agent(
    name="data_science_agent", # This is our Analytics Agent
    instruction=return_instructions_ds(), # Tells it how to do data analysis
    code_executor=VertexAiCodeExecutor(), # Allows it to run Python code!
    # ... other settings
)
```
Key things to note:
*   `name="data_science_agent"`: This is our Analytics specialist.
*   `instruction=return_instructions_ds()`: It has its own specific instructions for performing data science tasks.
*   `code_executor=VertexAiCodeExecutor()`: This is super important! It gives the Analytics Agent the ability to write and run Python code. So, it can perform calculations, use data science libraries (like pandas or numpy), and generate results.

If the Root Agent gives it sales numbers and asks for a trend, the Analytics Agent might write a small Python script to calculate that trend and then return the finding.

### 3. The BQML Agent (BigQuery ML Specialist)

*   **Role:** The "Machine Learning Maestro."
*   **Expertise:** Working with machine learning models directly within BigQuery, using BigQuery ML (BQML).
*   **How it works:** If your request involves creating, training, or using ML models that live inside BigQuery (e.g., "Predict next month's sales using our BQML forecasting model," or "Train a customer churn model with this data in BQML"), the Root Agent will call upon the BQML Agent. This agent knows how to construct and execute BQML commands.

Let's see a simplified setup from `data_science/sub_agents/bqml/agent.py`:

```python
# data_science/sub_agents/bqml/agent.py (Simplified)
from google.adk.agents import Agent
from .prompts import return_instructions_bqml # Agent's specific rules
from .tools import execute_bqml_code, check_bq_models, call_db_agent # Its BQML tools

# This 'root_agent' is specific to the BQML sub-agent's own setup
root_agent = Agent(
    name="bq_ml_agent",
    instruction=return_instructions_bqml(), # Tells it how to handle BQML tasks
    tools=[execute_bqml_code, check_bq_models, call_db_agent], # Tools for BQML
    # ... other settings
)
```
Here:
*   `name="bq_ml_agent"`: Identifies our BigQuery ML specialist.
*   `instruction=return_instructions_bqml()`: Provides its unique operating manual for BQML tasks.
*   `tools=[...]`: It has tools like `execute_bqml_code` to run BQML statements, `check_bq_models` to get information about existing models, and interestingly, `call_db_agent`. This means the BQML agent can itself ask the `Database Agent` to fetch data if needed for its ML tasks!

This shows that sub-agents can sometimes even use other sub-agents, forming a collaborative team.

## How the Root Agent Uses Its Team

Remember in Chapter 1, we saw the Root Agent's definition? It has a special parameter called `sub_agents`:

```python
# data_science/agent.py (Simplified snippet from Chapter 1)
from google.adk.agents import Agent
from .prompts import return_instructions_root
# Here we import our specialists!
from .sub_agents import bqml_agent, ds_agent, db_agent

root_agent = Agent(
    name="db_ds_multiagent", # Our main Root Agent
    instruction=return_instructions_root(), # Its main "rulebook"
    sub_agents=[bqml_agent, ds_agent, db_agent], # The list of its specialist team members!
    # ... other tools and settings
)
```
By listing `bqml_agent`, `ds_agent`, and `db_agent` in the `sub_agents` list, we're telling our Root Agent, "These are the experts you can call upon."

The file `data_science/sub_agents/__init__.py` helps organize these imports:
```python
# data_science/sub_agents/__init__.py
# This file makes it easy to import our sub-agents

from .bqml.agent import root_agent as bqml_agent
from .analytics.agent import root_agent as ds_agent # Renaming for clarity
from .bigquery.agent import database_agent as db_agent # Renaming for clarity

# This tells Python what names are available when we do "from .sub_agents import ..."
__all__ = ["bqml_agent", "ds_agent", "db_agent"]
```
This `__init__.py` file acts like a central hub for the sub-agents. It imports each specialist (sometimes renaming them for clarity, like `ds_agent` for the analytics agent) and then lists them in `__all__`. This makes it clean and easy for the main `agent.py` file to import all the necessary specialists.

When the Root Agent receives your request, its [Agent Prompts (Instructions)](03_agent_prompts__instructions_.md) guide it to decide if a specialist is needed and, if so, which one.

## The Workflow: A Specialist in Action

Let's imagine the Root Agent has decided to call the `Database Agent` for our sales query.

```mermaid
sequenceDiagram
    participant User
    participant RootAgent as Root Agent (Orchestrator)
    participant DatabaseAgent as DB Sub-Agent (Specialist)
    participant BigQuerySystem as BigQuery Database

    User->>RootAgent: "Total sales last month?"
    RootAgent->>RootAgent: Analyzes request, decides DB Agent is needed
    RootAgent->>DatabaseAgent: "Task: Get total sales for last month"
    DatabaseAgent->>DatabaseAgent: Consults its own instructions (prompts)
    DatabaseAgent->>DatabaseAgent: Uses NL2SQL tool to form a query: "SELECT SUM(sales) FROM sales_table WHERE month='last';"
    DatabaseAgent->>BigQuerySystem: Executes the SQL query
    BigQuerySystem-->>DatabaseAgent: (Sales Data: $50,000)
    DatabaseAgent-->>RootAgent: (Result: "Total sales last month were $50,000")
    RootAgent->>User: "Total sales last month were $50,000."
```

1.  The **User** asks the **Root Agent**.
2.  The **Root Agent** identifies that this requires data from the database and delegates the specific task to the **Database Agent**.
3.  The **Database Agent** receives the task. It uses its own internal instructions (its `prompt`) and specialized [Tools (Capabilities)](04_tools__capabilities_.md) (like an NL2SQL converter and a BigQuery executor tool) to:
    *   Understand the request more deeply ("total sales last month").
    *   Formulate the correct SQL query.
    *   Execute the query against the **BigQuery Database**.
4.  **BigQuery** returns the data to the **Database Agent**.
5.  The **Database Agent** packages this result and sends it back to the **Root Agent**.
6.  The **Root Agent** then presents this information to the **User**.

If the request also involved analysis (like finding a trend), the Root Agent would then take the data from the Database Agent and pass it to the Analytics Agent for the next step.

## Why is This "Team of Specialists" Approach So Good?

1.  **Expertise:** Each sub-agent is highly skilled in its specific area. The Database Agent knows databases; the Analytics Agent knows Python and stats. This leads to better, more accurate results.
2.  **Simplicity & Focus:** Each agent (including the Root Agent) has a simpler job. The Root Agent focuses on orchestrating, and sub-agents focus on their specialty. This makes their individual instructions ([Agent Prompts (Instructions)](03_agent_prompts__instructions_.md)) easier to write and manage.
3.  **Modularity & Maintainability:** If we want to improve how we talk to BigQuery, we can update just the Database Agent without touching the Analytics Agent or the Root Agent's core logic. This makes the system easier to develop and maintain.
4.  **Scalability & Extensibility:** Need a new capability, like interacting with a different type of data source or a new ML service? We can build a new specialist sub-agent for it and "plug it in" to the Root Agent!
5.  **Reusability:** A well-defined `Database Agent` could potentially be reused in other projects or by other orchestrating agents.

## Conclusion

Sub-Agents are the "doers" in our system, the specialists who handle the specific tasks delegated by the Root Agent. By having a team of experts—like a Database Agent for fetching data, an Analytics Agent for crunching numbers, and a BQML Agent for machine learning in BigQuery—our `data-science` project can tackle complex questions that require multiple steps and different kinds of expertise.

This modular, team-based approach is key to building powerful and flexible AI systems. The Root Agent directs the play, and the Sub-Agents perform their roles with precision.

Now that we've met the project manager (Root Agent) and its expert team (Sub-Agents), you might be wondering: how exactly do we *tell* these agents what to do and how to behave? That's where their "instructions" come in. In the next chapter, we'll explore [Agent Prompts (Instructions)](03_agent_prompts__instructions_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
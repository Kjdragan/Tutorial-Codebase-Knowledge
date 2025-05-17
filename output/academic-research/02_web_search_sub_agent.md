# Chapter 2: The Digital Detective - Web Search Sub-Agent

Welcome to Chapter 2! In our [previous chapter](01_academic_coordinator_agent.md), we met the **Academic Coordinator Agent**, the lead detective of our research team. It's great at understanding your main research paper and delegating tasks. Now, let's meet one of its most important specialists: the **Web Search Sub-Agent**.

## What's the Big Deal with Finding *Recent* Papers?

Imagine you found an amazing recipe for chocolate cake from a cookbook published in 1950. It's a classic! But you wonder, "Has anyone improved this recipe? Are there new baking techniques or ingredients that could make it even better?"

In the world of academic research, this happens all the time. A researcher publishes a groundbreaking paper (our "seminal paper"). Over time, other researchers read it, get inspired, and build upon that work. They might:
*   Test the original idea in new situations.
*   Combine it with other ideas.
*   Find new applications for it.
*   Even find limitations or ways to improve it!

If you only know about the original 1950s cake recipe, you're missing out on all the delicious variations and improvements made since then! The **Web Search Sub-Agent** is our specialist tasked with finding these "new recipes" – specifically, recent academic papers that refer back to (or "cite") your original seminal paper.

Its main job is to answer: **"What are the latest developments related to this foundational work?"**

## Meet the Web Search Sub-Agent: Your Online Sleuth

Think of the Web Search Sub-Agent as a research assistant who is incredibly skilled at using online search engines like Google, especially for academic purposes. You give it the details of your seminal paper, and its mission is to find other academic articles published very recently (usually in the current or previous year) that mention or build upon that original work.

**What it does:**
1.  **Takes the "Clue":** It receives information about the seminal paper from the Academic Coordinator Agent.
2.  **Scours the Web:** It uses web search tools to look for recent publications.
3.  **Focuses on "Recent":** It specifically targets papers from the current and previous year.
4.  **Builds a List:** It compiles a list of these recent, relevant papers.

This is like telling your librarian assistant, "Here's an important historical document. Can you find me all the articles published in the last year or two that reference it?"

**Why is this useful?**
*   **Stay Current:** It helps you understand the most up-to-date research in an area.
*   **Identify Trends:** You can see how the original idea is evolving.
*   **Find Inspiration:** Recent papers can spark new ideas for your own research.

## How It Gets the Job Done: An Example

Let's say your seminal paper is "The Future of Quantum Computing" by Dr. Innovate, published in 2010.

1.  **Input (from Academic Coordinator):**
    *   Seminal Paper Title: "The Future of Quantum Computing"
    *   Maybe some keywords or author names.

2.  **The Web Search Sub-Agent's Task:**
    *   Find academic papers published in the current year (e.g., 2025) or the previous year (e.g., 2024) that cite "The Future of Quantum Computing."

3.  **The Process (Simplified):**
    *   The agent might use search queries like:
        *   `"papers citing 'The Future of Quantum Computing' published 2025"`
        *   `"Dr. Innovate quantum computing" related works 2024`
        *   It will use its built-in search tool to execute these queries.
    *   It then looks through the search results, trying to confirm:
        *   Does this new paper actually cite the seminal paper?
        *   Was it published in the target years?

4.  **Output (to Academic Coordinator):**
    *   A list like:
        *   "Advances in Quantum Error Correction (2025)" - Cites "The Future of Quantum Computing"
        *   "Practical Applications of Quantum Algorithms (2024)" - Cites "The Future of Quantum Computing"

This list then goes back to the Academic Coordinator Agent, who will present it to you.

## A Look at the Code: Defining Our Sleuth

Just like our Academic Coordinator, the Web Search Sub-Agent is defined in code. It's a bit simpler because its job is very focused.

This snippet is from `academic_research/sub_agents/academic_websearch/agent.py`:

```python
# File: academic_research/sub_agents/academic_websearch/agent.py

from google.adk import Agent # A basic building block for agents
from google.adk.tools import google_search # The tool for searching the web

from . import prompt # This file contains the agent's detailed instructions

MODEL = "gemini-2.5-pro-preview-03-25" # The AI model it uses

academic_websearch_agent = Agent( # Notice 'Agent' instead of 'LlmAgent'
    model=MODEL,
    name="academic_websearch_agent",
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT, # Its specific instructions
    output_key="recent_citing_papers", # How its findings are labeled
    tools=[google_search], # The tools it can use (just Google Search here)
)
```

Let's break this down:

*   `Agent`: This is a simpler way to define an agent in our toolkit compared to `LlmAgent` (which the Academic Coordinator uses). It's often used for sub-agents that have a specific task and use tools, but don't manage other agents.
*   `model=MODEL`: Just like before, this tells the agent which AI model to use. We'll learn more in [LLM Model Configuration](07_llm_model_configuration.md).
*   `name="academic_websearch_agent"`: A unique name for this sub-agent.
*   `instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT`: This is crucial! It points to a detailed set of instructions (a "prompt") specifically for this agent, telling it *how* to search, *what* to look for, and *how* to format its findings. We'll peek at this next.
*   `output_key="recent_citing_papers"`: When this agent produces its list of papers, this key is used to label that output. The Academic Coordinator can then easily find and use this list.
*   `tools=[google_search]`: This tells the agent it has access to the `google_search` tool. This is how it actually performs web searches. We'll explore tools more in [Agent Tools](08_agent_tools.md).

## Under the Hood: The Agent's Search Strategy

So, what happens when the Academic Coordinator asks the Web Search Sub-Agent to find papers?

1.  **The Request:** The Academic Coordinator passes the details of the seminal paper (e.g., its title) to the Web Search Sub-Agent.
2.  **Consulting the "Playbook":** The Web Search Sub-Agent refers to its `instruction` (the `ACADEMIC_WEBSEARCH_PROMPT`). This prompt guides its entire process.
3.  **Determining Timeframe:** The prompt tells it to focus on the current and previous calendar years.
4.  **Formulating Queries:** Based on the seminal paper's details and its instructions, the agent (powered by the LLM) formulates specific search queries. For example, if the seminal paper is "Learning with Kernels" and the current year is 2025, it might think of:
    *   `"papers citing 'Learning with Kernels' published 2025"`
    *   `"recent works based on 'Learning with Kernels' year:2024"`
5.  **Using the Tool:** It uses the `google_search` tool to execute these queries on the internet.
6.  **Analyzing Results:** The agent examines the search results. It looks for:
    *   Clear evidence that a result cites the seminal paper.
    *   The publication date (is it in the target years?).
    *   Details like title, authors, and where it was published.
7.  **Refining the Search (if needed):** The prompt also guides it on what to do if it doesn't find enough papers initially (e.g., try different keywords, search specific academic sites).
8.  **Compiling the List:** It gathers all the relevant findings into a structured list.
9.  **Reporting Back:** It sends this list (labeled as `recent_citing_papers`) back to the Academic Coordinator.

Here's a simplified diagram of this flow:

```mermaid
sequenceDiagram
    participant AC as Academic Coordinator
    participant WSS as Web Search Sub-Agent
    participant LLM as WSS's Brain (LLM)
    participant GS as Google Search Tool

    AC->>WSS: Find recent papers citing "Seminal Paper X"
    WSS->>LLM: My prompt says to find papers for current/prev year citing "Seminal Paper X". How should I search?
    LLM->>WSS: Plan: Use Google Search tool with query: "papers citing Seminal Paper X published [current_year]"
    WSS->>GS: Execute search: "papers citing Seminal Paper X published 2025"
    GS-->>WSS: Here are search results.
    WSS->>LLM: Analyze these results based on my prompt.
    LLM->>WSS: Found: "Paper A (2025)", "Paper B (2025)"
    WSS->>LLM: My prompt says I need more. Try previous year and vary query.
    LLM->>WSS: Plan: Use Google Search tool with query: "related to Seminal Paper X author:Y year:2024"
    WSS->>GS: Execute search: "related to Seminal Paper X author:Y year:2024"
    GS-->>WSS: Here are more search results.
    WSS->>LLM: Analyze these results based on my prompt.
    LLM->>WSS: Found: "Paper C (2024)"
    WSS->>AC: Report: recent_citing_papers = [Paper A, Paper B, Paper C]
end
```

## The Agent's "Rulebook": A Glimpse at the Prompt

The `ACADEMIC_WEBSEARCH_PROMPT` (from `academic_research/sub_agents/academic_websearch/prompt.py`) is the detailed instruction manual for our Web Search Sub-Agent. It’s quite comprehensive, but here's a tiny peek at the *kind* of instructions it contains:

```
System Role: You are an AI assistant specializing in finding academic papers.

Objective:
  - Find academic papers published in the CURRENT_YEAR or PREVIOUS_YEAR.
  - These papers MUST cite "{seminal_paper_title}".
  - Try to find at least 5-10 papers if possible.

Tool to Use:
  - You MUST use the Google Search tool.

Basic Search Strategy:
  1. Identify the "{seminal_paper_title}".
  2. Determine CURRENT_YEAR and PREVIOUS_YEAR.
  3. Create search queries like:
     - "'papers citing {seminal_paper_title}' published CURRENT_YEAR"
     - "'{seminal_paper_title}' citations PREVIOUS_YEAR"
  4. Use the Google Search tool with these queries.
  5. From the results, extract Title, Authors, Publication Year, and Source.
  6. If you don't find enough, try variations:
     - Add author names from the seminal paper.
     - Search specific sites like scholar.google.com.

Output:
  - List the papers found, grouped by year.
  - For each paper, provide: Title, Authors, Year, Source, and a Link if found.
```

This is a very simplified version! The actual prompt (which you can find in the project files) is much more detailed. It includes instructions on how to handle cases where few results are found, how to format the output precisely, and how to be persistent. The placeholders like `{seminal_paper_title}` get filled in with the actual details of the paper you're interested in.

We'll learn much more about how these powerful instructions work in the [Agent Prompts](06_agent_prompts.md) chapter.

## Conclusion

The Web Search Sub-Agent is a crucial member of our research team. It acts like a diligent online detective, specifically focused on finding the most recent academic literature that builds upon a given seminal work. By leveraging web search tools and guided by a detailed prompt, it helps us understand the current state of research and discover how foundational ideas are evolving.

You've now met the Academic Coordinator (the team lead) and its specialist Web Search Sub-Agent (the online sleuth). What else can our team do? In the next chapter, we'll explore another specialist: the [New Research Sub-Agent](03_new_research_sub_agent.md), which helps us brainstorm where research might go *next*!

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
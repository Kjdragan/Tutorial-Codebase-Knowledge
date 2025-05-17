# Chapter 1: Meet Your Research Lead - The Academic Coordinator Agent

Welcome to the `academic-research` project! If you've ever found a fascinating older research paper and wondered, "What's happened since then? Where could this research go next?", then you're in the right place. This project aims to help you answer exactly those questions, and it all starts with our main "brain": the **Academic Coordinator Agent**.

Think of starting a new research journey like embarking on a detective case. You have an initial clue – your seminal paper. The Academic Coordinator Agent is like the lead detective assigned to this case. It's your main point of contact, helping you make sense of that first clue and figuring out where to look next.

## What is the Academic Coordinator Agent?

The Academic Coordinator Agent is the primary orchestrator of our research assistance process. It's the agent you'll interact with directly. Its main job is to:

1.  **Understand Your Request**: When you provide a seminal research paper, it first needs to understand what that paper is about.
2.  **Delegate Specialized Tasks**: Just like a lead detective doesn't do all the legwork alone, our Academic Coordinator has a team of specialist "sub-agents." It assigns specific tasks to them, such as:
    *   Finding recent papers that cite your seminal paper (like doing background checks).
    *   Suggesting new research ideas based on the findings (like profiling potential new leads).
3.  **Synthesize Information**: After the sub-agents report back, the Academic Coordinator gathers all the information and presents it to you in a clear, organized way – like a final case report.
4.  **Manage the Conversation**: It guides you through the process, asking for what it needs (like the seminal paper) and telling you what it's doing at each step.

In short, it's the friendly, intelligent interface that manages the entire research exploration journey for you.

## How It Works: A Simple Example

Let's imagine you have a groundbreaking paper from 2010 about renewable energy, and you want to know what's new.

1.  **You give the paper to the Academic Coordinator Agent.**
    *   **Input**: The PDF of your seminal paper (e.g., "RevolutionarySolarCells.pdf").
2.  **The Agent gets to work**:
    *   It first reads and analyzes your paper to understand its key contributions.
    *   It then calls on its specialist sub-agents:
        *   It asks the [Web Search Sub-Agent](02_web_search_sub_agent.md) to find recent academic articles (say, from the last two years) that have cited "RevolutionarySolarCells.pdf".
        *   Based on your original paper and the new findings, it asks the [New Research Sub-Agent](03_new_research_sub_agent.md) to brainstorm some potential future research directions.
3.  **The Agent presents its findings**:
    *   **Output (what you see)**:
        *   A summary of "RevolutionarySolarCells.pdf" (its main ideas, authors, etc.).
        *   A list of recent papers that build upon it.
        *   A set of suggestions for new research avenues in the field of revolutionary solar cells.

This entire process is managed by the Academic Coordinator, making your research exploration much smoother!

## Under the Hood: A Peek at the Code

The Academic Coordinator Agent is built using the `LlmAgent` class from a special toolkit designed for creating agents like this. Let's look at how it's defined in our project.

This snippet is from the `academic_research/agent.py` file:

```python
# File: academic_research/agent.py

from google.adk.agents import LlmAgent # The basic building block for our agent
from google.adk.tools.agent_tool import AgentTool # To give our agent "tools"

# These are our specialist helper agents, we'll learn more about them later!
from .sub_agents.academic_newresearch import academic_newresearch_agent
from .sub_agents.academic_websearch import academic_websearch_agent
from . import prompt # This file contains the agent's detailed instructions

MODEL = "gemini-2.5-pro-preview-03-25" # The AI model it uses

academic_coordinator = LlmAgent(
    name="academic_coordinator",
    model=MODEL,
    description=( # A brief explanation of what this agent does
        "analyzing seminal papers provided by the users, "
        "providing research advice, locating current papers "
        # ... (description continues)
    ),
    instruction=prompt.ACADEMIC_COORDINATOR_PROMPT, # Its main instructions
    tools=[ # Its team of helpers (sub-agents)!
        AgentTool(agent=academic_websearch_agent),
        AgentTool(agent=academic_newresearch_agent),
    ],
)
```

Let's break this down:

*   `LlmAgent`: This is the foundation. It means our Academic Coordinator is an agent powered by a Large Language Model (LLM), a type of AI that's great at understanding and generating text.
*   `name="academic_coordinator"`: This is just a unique name we give our agent.
*   `model=MODEL`: This tells the agent which specific AI model to use (in this case, a version of Gemini). We'll discuss models more in the [LLM Model Configuration](07_llm_model_configuration.md) chapter.
*   `description`: A short summary of the agent's purpose.
*   `instruction=prompt.ACADEMIC_COORDINATOR_PROMPT`: This is super important! It points to a detailed set of instructions (a "prompt") that tells the agent exactly how to behave, what to say, and when to use its tools. We'll explore this in depth in the [Agent Prompts](06_agent_prompts.md) chapter.
*   `tools=[...]`: This is the list of "specialist officers" our lead detective can call upon.
    *   `AgentTool(agent=academic_websearch_agent)`: Gives the coordinator access to the [Web Search Sub-Agent](02_web_search_sub_agent.md).
    *   `AgentTool(agent=academic_newresearch_agent)`: Gives it access to the [New Research Sub-Agent](03_new_research_sub_agent.md).
    *   We'll learn more about how agents use tools in the [Agent Tools](08_agent_tools.md) chapter.

You might also notice this line at the end of the `academic_research/agent.py` file:
```python
# File: academic_research/agent.py
# ... (previous code) ...

root_agent = academic_coordinator
```
This line tells our system that `academic_coordinator` is the main agent to start with when a user interacts with the `academic-research` project. This is a key part of how we define agents, which we'll touch upon in the [ADK Agent Definition](05_adk_agent_definition.md) chapter.

## The Coordinator's "Playbook": The Prompt

We mentioned the `instruction` parameter points to `prompt.ACADEMIC_COORDINATOR_PROMPT`. This prompt is like the detailed script or playbook for our Academic Coordinator. It's a long piece of text that guides the agent's every step.

Here's a tiny glimpse into what that prompt (from `academic_research/prompt.py`) looks like conceptually:

```
System Role: You are an AI Research Assistant...

Workflow:

Initiation:
  - Greet the user.
  - Ask for the seminal paper (PDF).

Seminal Paper Analysis:
  - Process the paper.
  - Present summary, authors, abstract, keywords, innovations...

Find Recent Citing Papers (Using academic_websearch):
  - Inform user you'll search.
  - Invoke the academic_websearch agent/tool...
  - Present results.

Suggest Future Research Directions (Using academic_newresearch):
  - Inform user you'll suggest directions.
  - Invoke the academic_newresearch agent/tool...
  - Present suggestions.

Conclusion:
  - Briefly conclude.
```

This prompt defines the entire [Workflow Orchestration](04_workflow_orchestration.md) that the Academic Coordinator manages. It tells the agent how to interact with you, how to analyze the paper, when to call its sub-agents, and how to present the information. It's the core logic driving its behavior. We'll dive much deeper into prompts in the [Agent Prompts](06_agent_prompts.md) chapter.

## Visualizing the Workflow

Here's a simple diagram showing how the Academic Coordinator interacts with you and its sub-agents:

```mermaid
sequenceDiagram
    participant U as User
    participant AC as Academic Coordinator
    participant WS as Web Search Sub-Agent
    participant NR as New Research Sub-Agent

    U->>AC: Here's my seminal paper (PDF)
    AC->>AC: Analyze seminal paper (summary, keywords, etc.)
    AC->>U: Here's a summary of your paper.
    AC->>U: I'll now search for recent citing papers.
    AC->>WS: Find papers citing [Seminal Paper ID] from last year
    WS-->>AC: Here are 5 recent papers.
    AC->>U: Found these recent papers: ...
    AC->>U: Now, I'll suggest future research directions.
    AC->>NR: Suggest research based on [Seminal Paper Info] and [Recent Papers]
    NR-->>AC: Here are some research ideas.
    AC->>U: Potential future research directions: ...
    AC->>U: Would you like to explore further?
end
```

This diagram illustrates the flow: you start by giving the paper to the Academic Coordinator (AC). The AC then processes it, talks to you, and then delegates tasks to the Web Search Sub-Agent (WS) and the New Research Sub-Agent (NR), finally compiling everything for you.

## Conclusion

And that's our Academic Coordinator Agent! It's the friendly and intelligent conductor of our research orchestra. It understands your initial request (the seminal paper), manages a team of specialist sub-agents to gather more information, and then brings everything together to give you a comprehensive view of the research landscape. It’s designed to be your primary guide in this journey of academic exploration.

You've now met the "lead detective." In the next chapter, we'll get to know one of its key specialists: the [Web Search Sub-Agent](02_web_search_sub_agent.md), which is responsible for finding those all-important recent papers.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
# Chapter 8: Agent Tools - Expanding Your Agent's Abilities

Welcome to Chapter 8! In our [previous chapter on LLM Model Configuration](07_llm_model_configuration.md), we learned about choosing the "brain" or Large Language Model (LLM) that powers our agents. We saw that our agents use a powerful "engine" like `gemini-2.5-pro-preview-03-25` to understand instructions and "think."

But what if an agent needs to do something more than just "think" or generate text? What if it needs to search the internet, perform a calculation, or even ask another specialized agent for help? For these kinds of tasks, agents need **Tools**.

Imagine you're a skilled craftsperson (our main agent). You have excellent general knowledge and skills (thanks to your LLM brain and [Agent Prompts](06_agent_prompts.md)). But to build something amazing, you often need specialized equipment – a power drill, a specific saw, a measuring tape, or even a colleague who's an expert in a particular technique. Agent Tools are exactly like this specialized equipment and expert colleagues for our AI agents!

## What are Agent Tools? Your Agent's Special Equipment

**Agent Tools** are specific capabilities or helper modules that an agent can use to perform actions or gather information that it can't do on its own.
*   They can be **external utilities**, like a tool to search Google.
*   They can even be **other agents** that are specialized for a particular task (e.g., our Academic Coordinator agent uses the Web Search Sub-Agent as one of its tools).

Think of it this way:
*   **Your Agent**: A talented chef.
*   **Agent's LLM Brain**: The chef's culinary knowledge and creativity.
*   **Agent's Prompt**: The chef's detailed recipe and instructions for a dish.
*   **Agent Tools**:
    *   A food processor (an external utility like `google_search`).
    *   A pastry chef assistant (another agent specialized in desserts).

Tools **extend an agent's functionality** beyond what the LLM alone can do. They allow an agent to interact with the outside world, use other software, or delegate tasks to other specialized systems.

## Giving Your Agent Tools: The `tools` Parameter

How does an agent get its tools? When we define an agent using the ADK (as we saw in the [ADK Agent Definition](05_adk_agent_definition.md) chapter), we can give it a list of tools it's allowed to use. This is done using the `tools` parameter in the agent's definition.

It's like stocking a workshop with specific equipment before the craftsperson starts their project.

## Two Main Kinds of Tools in Our `academic-research` Project

In our `academic-research` project, we see two primary ways tools are used:

### 1. External Utilities: The Ready-Made Power Drill (`google_search`)

Some tools are like standard, off-the-shelf equipment that many agents might find useful. The Agent Development Kit (ADK) provides some of these pre-built tools. A great example is the `google_search` tool.

Our [Web Search Sub-Agent](02_web_search_sub_agent.md) needs to search the internet for recent academic papers. Its LLM brain can't directly browse the web. So, we equip it with the `google_search` tool.

Let's look at how the `academic_websearch_agent` is given this tool in `academic_research/sub_agents/academic_websearch/agent.py`:

```python
# File: academic_research/sub_agents/academic_websearch/agent.py

from google.adk import Agent
from google.adk.tools import google_search # Importing the pre-built tool

from . import prompt

MODEL = "gemini-2.5-pro-preview-03-25"

academic_websearch_agent = Agent(
    model=MODEL,
    name="academic_websearch_agent",
    instruction=prompt.ACADEMIC_WEBSEARCH_PROMPT,
    output_key="recent_citing_papers",
    tools=[google_search], # Here's the tool!
)
```
*   `from google.adk.tools import google_search`: This line imports the ready-to-use `google_search` tool from the ADK's collection of tools.
*   `tools=[google_search]`: This tells the `academic_websearch_agent` that it has the `google_search` tool in its "toolbox." Now, when its [Agent Prompts](06_agent_prompts.md) instruct it to find information online, its LLM can decide to use this tool.

### 2. Other Agents as Specialized Colleagues: The Expert Consultant (`AgentTool`)

Sometimes, the best "tool" for a job is another agent that has its own specialized skills. Our main [Academic Coordinator Agent](01_academic_coordinator_agent.md) is like a project manager. It needs to:
1.  Find recent papers (a job for the [Web Search Sub-Agent](02_web_search_sub_agent.md)).
2.  Suggest new research ideas (a job for the [New Research Sub-Agent](03_new_research_sub_agent.md)).

The Academic Coordinator doesn't do these specialized tasks itself. Instead, it uses the `academic_websearch_agent` and `academic_newresearch_agent` as its tools!

To make one agent usable as a tool by another, we wrap it with `AgentTool`. Let's see this in the definition of `academic_coordinator` from `academic_research/agent.py`:

```python
# File: academic_research/agent.py
# ... (other imports)
from google.adk.tools.agent_tool import AgentTool # For wrapping agents as tools

# These are our specialist helper agents
from .sub_agents.academic_newresearch import academic_newresearch_agent
from .sub_agents.academic_websearch import academic_websearch_agent

# ... (MODEL definition)

academic_coordinator = LlmAgent(
    name="academic_coordinator",
    # ... (model, description, instruction)
    tools=[ # Its team of specialist "tools"!
        AgentTool(agent=academic_websearch_agent),
        AgentTool(agent=academic_newresearch_agent),
    ],
)
```
*   `from google.adk.tools.agent_tool import AgentTool`: This imports the `AgentTool` class, which is used to "package" an existing agent so it can be used as a tool.
*   `tools=[...]`: This list now contains:
    *   `AgentTool(agent=academic_websearch_agent)`: This tells the Academic Coordinator, "You have a tool which is actually the `academic_websearch_agent` itself."
    *   `AgentTool(agent=academic_newresearch_agent)`: Similarly, it gives the Coordinator access to the `academic_newresearch_agent`.

Now, the Academic Coordinator can delegate specific tasks to these sub-agents, just like a manager delegates work to specialists in their team.

## How Does an Agent Know *When* to Use a Tool?

Giving an agent a tool is like putting a power drill in its toolbox. But how does the agent know when to pick it up and use it?

This is where the agent's "brain" (the LLM) and its "instruction manual" (the [Agent Prompts](06_agent_prompts.md)) work together:
1.  **The Prompt Guides**: The agent's prompt often contains instructions like, "If you need to find recent information, use the web search tool," or "To generate research ideas, consult the new research specialist tool."
2.  **The LLM Decides**: When the agent is working on a task, its LLM processes the current situation and the instructions from the prompt. Based on this, the LLM makes a decision: "Aha! For this part of the task, I need to use tool X."
3.  **The ADK Executes**: Once the LLM decides to use a tool, the Agent Development Kit (ADK) framework handles the actual "calling" of the tool and getting the result back.

So, it's not random! The use of tools is a deliberate decision made by the agent's LLM, guided by the explicit instructions you provide in its prompt.

## Under the Hood: A Tool in Action

Let's imagine you ask the Academic Coordinator Agent: "Analyze this seminal paper on 'Quantum Dots' and find recent related articles."

Here's a simplified step-by-step of what might happen:

1.  **User Request**: You give the seminal paper PDF and your request to the `academic_coordinator` agent.
2.  **Coordinator's Prompt**: The `academic_coordinator` consults its `ACADEMIC_COORDINATOR_PROMPT`. This prompt has a workflow section for "Find Recent Citing Papers."
3.  **LLM Decision (Coordinator)**: The Coordinator's LLM reads the prompt. The prompt says to use the `academic_websearch_agent` tool for finding recent papers. The LLM decides: "Okay, I need to use my `academic_websearch_agent` tool and tell it to find papers related to 'Quantum Dots'."
4.  **Tool Invocation (ADK)**: The ADK system helps the `academic_coordinator` call the `academic_websearch_agent` (which is one of its tools), passing along the necessary information (e.g., "Quantum Dots").
5.  **Sub-Agent at Work (`academic_websearch_agent`)**:
    *   The `academic_websearch_agent` gets activated. It consults *its own* `ACADEMIC_WEBSEARCH_PROMPT`.
    *   Its prompt tells it to use the `google_search` tool to find papers from the current/previous year.
    *   Its LLM decides: "I need to use my `google_search` tool with queries like 'Quantum Dots recent papers 2024'."
    *   The ADK helps the `academic_websearch_agent` use the actual `google_search` tool.
6.  **External Tool Executes (`google_search`)**: The `google_search` tool interacts with Google's search engine.
7.  **Results Flow Back**:
    *   Google Search returns results to the `google_search` tool.
    *   The `google_search` tool passes these results to the `academic_websearch_agent`.
    *   The `academic_websearch_agent` processes these results (as per its prompt) and prepares a list of relevant papers.
    *   This list is then returned to the `academic_coordinator` as the output of the `academic_websearch_agent` tool.
8.  **Coordinator Continues**: The `academic_coordinator` now has the list of recent papers. It continues following its own prompt, which might say to present these papers to you, and then perhaps call the `academic_newresearch_agent` tool.

Here's a diagram visualizing this flow:

```mermaid
sequenceDiagram
    participant U as User
    participant ACA as Academic Coordinator
    participant ACALLM as ACA's LLM Brain
    participant ACAPrompt as ACA's Prompt
    participant WSTool as Web Search Sub-Agent (as Tool)
    participant WSPrompt as Web Search Sub-Agent's Prompt
    participant GS utilidad as Google Search (ADK Utility)

    U->>ACA: "Find recent papers on Quantum Dots."
    ACA->>ACAPrompt: Consult my instructions.
    ACAPrompt-->>ACA: Step: Use 'Web Search Sub-Agent' tool.
    ACA->>ACALLM: My prompt says find papers. How?
    ACALLM-->>ACA: Plan: Invoke 'Web Search Sub-Agent' tool for "Quantum Dots".
    
    ACA->>WSTool: Find papers related to "Quantum Dots".
    WSTool->>WSPrompt: Consult my instructions.
    WSPrompt-->>WSTool: Step: Use 'google_search' utility.
    WSTool->>GS utilidad: Execute search: "recent Quantum Dots papers"
    GS utilidad-->>WSTool: Raw search results.
    WSTool->>WSTool: Process results (as per WSPrompt).
    WSTool-->>ACA: Here's a list of relevant papers.
    
    ACA->>ACALLM: I have the papers. What next?
    ACALLM-->>ACA: Plan: Present papers to user (as per ACAPrompt).
    ACA->>U: "Found these recent papers on Quantum Dots: ..."
end
```
This shows how a tool (even if it's another agent) can have its own tools and logic, all orchestrated by prompts and LLM decisions. The ADK framework handles the "plumbing" to make these tool calls work smoothly.

## Why Are Tools So Useful? The Benefits

Equipping agents with tools offers several powerful advantages:

*   **Extensibility**: Agents aren't limited to just what the LLM knows or can generate by itself. They can access up-to-date information (like via web search) or perform actions in other systems.
*   **Modularity**: Complex problems can be broken down. Instead of one giant agent trying to do everything, you can have specialized agents (tools) that are experts at one particular thing. This makes the system easier to build, test, and maintain.
*   **Access to Real-World Information & Actions**: Tools can connect agents to live data sources (like Google Search), databases, or other software APIs (Application Programming Interfaces).
*   **Specialization**: Sub-agents, acting as tools, can be highly fine-tuned for their specific tasks, leading to better performance on those tasks.
*   **Code Reusability**: A well-defined tool (like `google_search` or a specialized sub-agent) can be used by many different parent agents.

Tools transform agents from being just "thinkers" into "doers" that can interact with and leverage a much wider range of capabilities.

## Conclusion

Agent Tools are like the special equipment and expert assistants that make our AI agents far more capable. They allow agents to perform specific actions, gather external information, or delegate complex sub-tasks to other specialized agents. In our `academic-research` project, we see this with the `google_search` utility empowering the [Web Search Sub-Agent](02_web_search_sub_agent.md), and with sub-agents themselves becoming powerful tools for the main [Academic Coordinator Agent](01_academic_coordinator_agent.md). These tools are specified in an agent's definition and are used intelligently by the agent's LLM, guided by its [Agent Prompts](06_agent_prompts.md).

We've now seen how our agents are defined, get their instructions, choose their "brains," and use tools. But how do we actually run this whole system? How is it made available for you to use? In the next and final chapter of this tutorial series, we'll get a glimpse into [Vertex AI Deployment](09_vertex_ai_deployment.md), which is how our `academic-research` project can be hosted and run as a service.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
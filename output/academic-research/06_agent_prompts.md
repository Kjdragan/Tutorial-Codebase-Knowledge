# Chapter 6: Agent Prompts - The Agent's Detailed "How-To" Guide

Welcome to Chapter 6! In our [previous chapter on ADK Agent Definition](05_adk_agent_definition.md), we learned how to create the basic blueprint for our AI agents. We saw that a crucial part of this blueprint is the `instruction` parameter, which points to the agent's detailed instructions. Now, we're going to dive deep into what those instructions, known as **Agent Prompts**, really are and why they're so important.

Imagine you've hired a new, very smart assistant (our AI agent). You've given them a job title (their `name`) and access to some tools. But how do they know *exactly* what to do, how to talk to you, what steps to follow for a complex task, or what their final report should look like? That's where their detailed "How-To" guide – the Agent Prompt – comes in!

## What's an Agent Prompt? Your Agent's Brain and Playbook!

At its heart, an **Agent Prompt** is a carefully crafted piece of text that tells a Large Language Model (LLM) how to behave and what to do when it's acting as a specific agent. Think of it as the "source code" that defines the agent's personality, workflow, and decision-making process.

For our `academic-research` project, prompts are critical. Consider our [Academic Coordinator Agent](01_academic_coordinator_agent.md). How does it know to:
1.  Greet you politely?
2.  Ask for your seminal research paper?
3.  Analyze the paper and summarize its key points?
4.  Then, decide to call the [Web Search Sub-Agent](02_web_search_sub_agent.md) to find recent articles?
5.  And *after that*, call the [New Research Sub-Agent](03_new_research_sub_agent.md) to brainstorm future ideas?
6.  And finally, present all this information back to you in a structured way?

The answer: It's all written down in its Agent Prompt!

## The Two Sides of a Prompt: Job Description & Operating Manual

A good agent prompt is like a combination of a very detailed **job description** and a comprehensive **Standard Operating Procedure (SOP) manual** for an employee (our AI agent).

Let's break down these two aspects:

### 1. The "Job Description" Part: Defining Role and Purpose

This part of the prompt sets the stage for the agent.
*   **Role/Persona**: It tells the LLM what kind_of assistant it should be. For example, the prompt for our `academic_coordinator` starts with:
    ```text
    System Role: You are an AI Research Assistant. Your primary function is to analyze a seminal paper...
    ```
    This helps the LLM adopt the correct tone, style, and even the type of knowledge it should focus on. It's like telling an actor what character they're playing.
*   **Overall Objectives**: It clearly states the agent's main goals. What is it ultimately trying to achieve for the user?

### 2. The "SOP Manual" Part: Detailing Actions and Procedures

This is where the prompt gets really specific, guiding the agent step-by-step.
*   **Workflow/Sequence of Steps**: It lays out the order of operations. As we saw in [Workflow Orchestration](04_workflow_orchestration.md), the `ACADEMIC_COORDINATOR_PROMPT` defines a multi-step process from greeting the user to presenting final results.
    *   Example: "First, greet the user. Then, ask for the seminal paper. Once the paper is provided, analyze it..."
*   **Task-Specific Instructions**: For each step in the workflow, it details *how* to perform that task.
    *   Example (from `ACADEMIC_COORDINATOR_PROMPT` for analyzing the seminal paper):
        ```text
        Present the extracted information clearly under the following distinct headings:
        Seminal Paper: [Display Title, Primary Author(s), Publication Year]
        Authors: [List all authors...]
        Abstract: [Display the full abstract text]
        ```
*   **Tool Usage**: It instructs the agent when and how to use its available [Agent Tools](08_agent_tools.md).
    *   Example (from `ACADEMIC_COORDINATOR_PROMPT`):
        ```text
        Find Recent Citing Papers (Using academic_websearch):
          Inform the user you will now search for recent papers...
          Action: Invoke the academic_websearch agent/tool.
        ```
*   **Output Formatting**: It specifies how the agent should structure its responses or any information it generates. This ensures consistency and makes the output easy for users (or other agents) to understand.
*   **Communication Protocols**: It guides how the agent should interact with the user – what to say at different stages, how to ask for clarification, etc.

Essentially, the prompt is the agent's comprehensive guide to doing its job effectively and correctly.

## Where Do Prompts Live in Our Project?

In `academic-research`, we keep our prompts neatly organized in Python files, usually named `prompt.py` within the respective agent's directory.

For example:
*   The prompt for our main coordinator is in `academic_research/prompt.py` as `ACADEMIC_COORDINATOR_PROMPT`.
*   The prompt for the web search sub-agent is in `academic_research/sub_agents/academic_websearch/prompt.py` as `ACADEMIC_WEBSEARCH_PROMPT`.

Here's how `ACADEMIC_COORDINATOR_PROMPT` is defined (conceptually) in `academic_research/prompt.py`:

```python
# File: academic_research/prompt.py

ACADEMIC_COORDINATOR_PROMPT = """
System Role: You are an AI Research Assistant...
Workflow:
Initiation:
  - Greet the user.
  - Ask for the seminal paper (PDF).
# ... (many more detailed instructions follow)
"""
# This is a very long string containing all the instructions.
```
This Python variable `ACADEMIC_COORDINATOR_PROMPT` holds the entire text of the instructions.

## Connecting Prompts to Agents: The `instruction` Parameter

Remember from the [ADK Agent Definition](05_adk_agent_definition.md) chapter, when we define an agent, we use the `instruction` parameter? This is where we link the agent to its prompt!

Let's look at the `academic_coordinator` definition again:

```python
# File: academic_research/agent.py
from google.adk.agents import LlmAgent
from . import prompt # Imports all prompts from prompt.py

# ... (other imports and model definition) ...

academic_coordinator = LlmAgent(
    name="academic_coordinator",
    model="gemini-2.5-pro-preview-03-25", # The AI model it uses
    description=("..."),
    instruction=prompt.ACADEMIC_COORDINATOR_PROMPT, # THIS IS THE LINK!
    tools=[ ... ],
)
```
The line `instruction=prompt.ACADEMIC_COORDINATOR_PROMPT` tells our `academic_coordinator` agent: "Your complete set of instructions – your job description and SOP manual – is located in the `ACADEMIC_COORDINATOR_PROMPT` variable."

## Placeholders: Making Prompts Dynamic

Sometimes, prompts need to refer to information that isn't known until the agent is actually running. For example, the `academic_websearch_agent` needs to know the *specific* seminal paper to search for. Prompts handle this using **placeholders**, often denoted with curly braces `{like_this}`.

Consider this snippet from `academic_research/sub_agents/academic_websearch/prompt.py`:

```python
# Snippet from academic_research/sub_agents/academic_websearch/prompt.py
ACADEMIC_WEBSEARCH_PROMPT = """
Role: You are a highly accurate AI assistant...

Objective: Identify and list academic papers that cite the seminal paper '{seminal_paper}' AND
were published ... in the current year or the previous year.

Instructions:
Identify Target Paper: The seminal paper being cited is {seminal_paper}.
...
"""
```
When the Academic Coordinator calls the `academic_websearch_agent`, it will provide the actual title or details of the seminal paper. The ADK framework and the LLM will then substitute this actual information wherever `{seminal_paper}` appears in the prompt.

If the seminal paper is "RevolutionarySolarCells.pdf", the LLM effectively sees:
"...cite the seminal paper 'RevolutionarySolarCells.pdf'..."
"...The seminal paper being cited is RevolutionarySolarCells.pdf."

This makes prompts incredibly flexible and reusable for different inputs!

## Under the Hood: How an LLM Uses a Prompt

So, what actually happens when an agent needs to act? How does the LLM use the prompt?

1.  **Agent Activation**: The agent is triggered, either by a user's message or by another agent.
2.  **Prompt Retrieval**: The system fetches the agent's assigned prompt (the long string of text).
3.  **Context Combination**: The agent's prompt is combined with:
    *   The current user input (e.g., "Tell me about this paper...").
    *   Any relevant conversation history (so the agent remembers what was said before).
    *   Any data passed from a calling agent (if it's a sub-agent).
4.  **Sending to LLM**: This whole package of information (prompt + current query + history) is sent to the Large Language Model (e.g., Gemini) that the agent is configured to use. We'll learn more about this in [LLM Model Configuration](07_llm_model_configuration.md).
5.  **LLM Processing**: The LLM reads *everything*. It uses the prompt as its primary guide on how to interpret the current query and what to do next.
6.  **LLM Response Generation**: Based on the instructions in the prompt and the specifics of the query, the LLM generates a response. This could be:
    *   Text to show to the user.
    *   A decision to use one of its [Agent Tools](08_agent_tools.md).
    *   An internal thought process leading to further actions.
7.  **Action/Output**: The agent then acts on the LLM's generated response.

Here's a simple diagram illustrating this flow:

```mermaid
sequenceDiagram
    participant User
    participant AgentSystem as Agent System (ADK)
    participant PromptText as Agent's Stored Prompt
    participant LLM as Large Language Model

    User->>AgentSystem: "Find recent papers on 'Quantum Entanglement'"
    AgentSystem->>PromptText: Load prompt for 'WebSearchAgent'
    PromptText-->>AgentSystem: Here is ACADEMIC_WEBSEARCH_PROMPT
    Note over AgentSystem, LLM: AgentSystem combines prompt, user query, and history.
    AgentSystem->>LLM: Send combined context: (Prompt text + "User query: Find recent papers on 'Quantum Entanglement'")
    LLM->>LLM: Reads prompt instructions. Understands it needs to search.
    LLM-->>AgentSystem: Plan: "Use Google Search tool with query: 'recent papers Quantum Entanglement'" (This is guided by the prompt's instructions on tool use)
    AgentSystem->>User: "Okay, I will search for recent papers on 'Quantum Entanglement'..." (And then uses the search tool)
end
```
The prompt is the constant guide for the LLM, ensuring it stays on task and follows the desired procedures.

## Why Are Well-Crafted Prompts So Crucial?

*   **Clarity and Consistency**: A good prompt leads to predictable and reliable agent behavior. If the instructions are vague, the agent's actions might be unpredictable.
*   **Control**: Prompts give you fine-grained control over what the agent says, does, and how it presents information.
*   **Effectiveness**: The quality of the prompt directly impacts how well the LLM can perform the desired task. A detailed, well-structured prompt can enable an LLM to handle complex, multi-step reasoning and actions.
*   **"Prompt Engineering"**: Designing and refining prompts is a key skill in developing powerful AI applications. It's an iterative process: you write a prompt, test it, see how the agent behaves, and then tweak the prompt to improve performance.

Without clear and comprehensive prompts, our agents would be like smart assistants without any direction – full of potential but unsure how to apply it to the tasks at hand.

## Conclusion

Agent Prompts are the heart and soul of our AI agents' intelligence and behavior. They are the detailed instruction manuals, job descriptions, and scripts that guide the Large Language Model. By carefully crafting these text-based blueprints, we define each agent's role, workflow, communication style, and how it uses its tools. The `instruction` parameter in the [ADK Agent Definition](05_adk_agent_definition.md) is what links an agent to its specific prompt, bringing it to life.

We've seen that prompts tell the agent *what to do* and *how to do it*. These instructions are then processed by a powerful Large Language Model. But which LLM should we use? And can we adjust its settings? That's exactly what we'll explore in the next chapter: [LLM Model Configuration](07_llm_model_configuration.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
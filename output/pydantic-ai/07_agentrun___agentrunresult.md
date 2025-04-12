# Chapter 7: AgentRun / AgentRunResult - Watching the Process and Getting the Result

In [Chapter 6: RunContext](06_runcontext.md), we learned how `pydantic-ai` provides a "briefing" (`RunContext`) to individual parts of an [Agent](01_agent.md)'s job, like a [Tool](05_tool.md), giving it the specific information it needs at that moment.

But what if you want to see the *entire* process unfold? Or what if you just need the final, complete report once the Agent has finished its task? How do we represent the Agent's execution itself, both while it's happening and after it's done?

This is where `AgentRun` and `AgentRunResult` come in. They help us track and understand the full lifecycle of an Agent's task.

## What's the Big Idea? Live Stream vs. Final Report

Imagine an Agent's task is like assembling a complex piece of furniture.

*   **`AgentRun` is like watching a live video stream** of the assembly process. You can see each step as it happens: laying out the parts, putting screws in, checking the instructions, maybe even calling a friend (using a [Tool](05_tool.md)) for help. You can follow along in real-time.
*   **`AgentRunResult` is like the final, assembled piece of furniture**, along with a report detailing how much time it took, which tools were used, and maybe the instruction manual with notes. It's the complete outcome delivered after the process is finished.

Why do we need both? Sometimes you want to observe the process for debugging or to show progress to a user (like the live stream). Other times, you just care about the final product and the summary report.

*   **`AgentRun`**: Represents an *active, ongoing execution* of an [Agent](01_agent.md). It allows you to iterate over the individual steps the Agent is taking (like talking to the [Model](03_model.md) or using a [Tool](05_tool.md)).
*   **`AgentRunResult`**: Holds the *final outcome* once the Agent's run is complete. It contains the final structured data (`result.data`), information about resource usage (like tokens), and the complete history of [Messages](02_message___part.md) exchanged.

## Watching the Live Stream: Using `AgentRun` with `agent.iter()`

If you want to see the steps of the Agent's execution as they happen, you use the `agent.iter()` method within an `async with` block. This gives you an `AgentRun` object that you can iterate over.

Let's run our simple "capital city" example from [Chapter 1](01_agent.md), but this time, we'll watch the steps using `agent.iter()`.

```python
# examples/pydantic_ai_examples/pydantic_model.py (Modified for iteration)
from pydantic import BaseModel
from pydantic_ai import Agent
import os
import asyncio # Need asyncio for async operations

class MyModel(BaseModel):
    city: str
    country: str

# Assume 'agent' is defined as before:
# model_string = os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o')
# agent = Agent(model_string, result_type=MyModel, instrument=True)

async def watch_the_agent():
    # Define the agent (replace with your actual setup)
    model_string = os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o')
    agent = Agent(model_string, result_type=MyModel, instrument=True)

    prompt = 'The windy city in the US of A.'
    print(f"--- Starting Agent run for: '{prompt}' ---")

    nodes_visited = []
    # Use agent.iter() to get the live AgentRun
    async with agent.iter(prompt) as agent_run:
        # Iterate over the steps (nodes) in the Agent's process
        async for node in agent_run:
            print(f"Step executed: {type(node).__name__}")
            nodes_visited.append(type(node).__name__)
            # You could inspect the 'node' object here for more details

    # The 'async with' block finishes when the agent run is complete
    print("--- Agent run finished ---")

    # After the run, the result is available on the agent_run object
    final_result = agent_run.result
    if final_result:
        print(f"Final Data: {final_result.data}")
        print(f"Total Usage: {final_result.usage()}")
    else:
        print("Agent run did not complete successfully.") # Should not happen here

# To run the async function
# asyncio.run(watch_the_agent())
```

**How to run this:** Since `watch_the_agent` is an `async` function, you'd typically run it like this in a script:

```python
if __name__ == "__main__":
    try:
        asyncio.run(watch_the_agent())
    except Exception as e:
        # Handle potential errors during API calls, etc.
        print(f"An error occurred: {e}")
```

**Expected Output (Conceptual):**

```text
--- Starting Agent run for: 'The windy city in the US of A.' ---
Step executed: UserPromptNode
Step executed: ModelRequestNode
Step executed: CallToolsNode
Step executed: End
--- Agent run finished ---
Final Data: city='Chicago' country='USA'
Total Usage: Usage(total_requests=1, ...)
```

**Explanation:**

1.  **`async with agent.iter(prompt) as agent_run:`**: This starts the Agent's process for the given prompt and gives us the `agent_run` object, representing the live execution.
2.  **`async for node in agent_run:`**: We loop through the `agent_run`. Each iteration yields a `node` object representing a completed step in the Agent's internal workflow (its "graph").
3.  **`print(f"Step executed: {type(node).__name__}")`**: We print the type of each step (node) visited. Common node types include:
    *   `UserPromptNode`: Processes the initial user input and system prompts.
    *   `ModelRequestNode`: Represents sending a request to the LLM ([Model](03_model.md)).
    *   `CallToolsNode`: Represents receiving the LLM's response and potentially deciding to call [Tools](05_tool.md) or processing the final result.
    *   `End`: Represents the successful completion of the run.
4.  **`final_result = agent_run.result`**: *After* the `async with` block finishes (meaning the run is complete), the `agent_run` object automatically gets populated with the final result, which we store in `final_result`.
5.  **Accessing Result Details:** We then access the structured data (`final_result.data`) and usage information (`final_result.usage()`) from the completed result.

Iterating with `AgentRun` is useful for:
*   Logging the Agent's internal steps.
*   Debugging complex Agent behavior.
*   Building user interfaces that show the Agent "thinking".
*   Performing actions at specific points during the run.

## Getting the Final Report: Using `AgentRunResult`

Often, you don't need to watch the live stream; you just want the final outcome. When you use `agent.run()` or `agent.run_sync()`, the Agent runs its entire process internally and directly returns the completed `AgentRunResult`.

```python
# examples/pydantic_ai_examples/pydantic_model.py (Using run_sync)
from pydantic import BaseModel
from pydantic_ai import Agent
import os

class MyModel(BaseModel):
    city: str
    country: str

# Assume 'agent' is defined as before:
model_string = os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o')
print(f'Using model: {model_string}')
agent = Agent(model_string, result_type=MyModel, instrument=True)

prompt = 'The windy city in the US of A.'

# Run the agent synchronously and get the final result directly
result: AgentRunResult[MyModel] = agent.run_sync(prompt)

# Access the structured data
print(f"Final Data: {result.data}")

# Access the total usage statistics
print(f"Total Usage: {result.usage()}")

# Access the full conversation history
print("\n--- All Messages ---")
all_msgs = result.all_messages()
for msg in all_msgs:
    print(f" - Type: {type(msg).__name__}, Parts: {len(msg.parts)}")

# Access only the messages generated during *this* specific run
print("\n--- New Messages (from this run) ---")
new_msgs = result.new_messages()
for msg in new_msgs:
    print(f" - Type: {type(msg).__name__}, Parts: {len(msg.parts)}")
```

**Expected Output (Conceptual):**

```text
Using model: openai:gpt-4o
Final Data: city='Chicago' country='USA'
Total Usage: Usage(total_requests=1, model_requests=1, total_input_tokens=..., total_output_tokens=..., ...)

--- All Messages ---
 - Type: ModelRequest, Parts: 1
 - Type: ModelResponse, Parts: 1

--- New Messages (from this run) ---
 - Type: ModelRequest, Parts: 1
 - Type: ModelResponse, Parts: 1
```

**Explanation:**

1.  **`result = agent.run_sync(prompt)`**: This runs the entire Agent process and waits for it to complete. It returns an `AgentRunResult` object directly. (The async version `agent.run()` does the same but returns an awaitable).
2.  **`result.data`**: Accesses the final, validated Pydantic model (`MyModel` instance) that the Agent produced.
3.  **`result.usage()`**: Retrieves a `Usage` object containing details about token counts, number of model requests, etc., for the entire run. We'll cover [Usage](08_usage.md) in the next chapter.
4.  **`result.all_messages()`**: Returns a list of *all* [Message](02_message___part.md) objects exchanged during the run (including any history you might have passed in). This shows the complete conversation context.
5.  **`result.new_messages()`**: Returns only the list of [Messages](02_message___part.md) that were generated during *this specific run*. This is useful if you passed in previous history and only want to see what happened *now*.

Using `AgentRunResult` is the standard way to:
*   Get the final structured output from the Agent.
*   Track costs and performance using usage data.
*   Store or display the conversation history.

## How It Works Under the Hood

Internally, `pydantic-ai` uses a powerful library called `pydantic-graph` (which we'll touch on later in [Chapter 12](12_graph__pydantic_graph_.md)) to manage the Agent's execution flow.

1.  **Graph Definition:** When you create an `Agent`, it defines an internal execution graph (like a flowchart) with nodes like `UserPromptNode`, `ModelRequestNode`, `CallToolsNode`, etc. This logic lives primarily in `pydantic_ai/_agent_graph.py`.
2.  **`agent.iter()` Starts Graph Run:** Calling `agent.iter()` initializes and starts a `GraphRun` from the `pydantic-graph` library, passing it the initial state (like message history, usage) and dependencies.
3.  **`AgentRun` Wraps `GraphRun`:** The `AgentRun` object you get is essentially a user-friendly wrapper around this active `GraphRun`.
4.  **Iteration Executes Nodes:** When you `async for node in agent_run`, you are iterating through the nodes executed by the underlying `GraphRun`.
5.  **Graph Reaches `End`:** The `GraphRun` continues until it reaches a special `End` node, which contains the final result data (e.g., the `MyModel` instance or the plain string).
6.  **Result Population:** When the `GraphRun` finishes, the `AgentRun` object captures the final state (including the final `Usage`) and the output from the `End` node.
7.  **`AgentRunResult` Creation:** It packages this final data, state, and usage information into an `AgentRunResult` object, which becomes available via `agent_run.result`.
8.  **`agent.run()` / `run_sync()`:** These methods simply perform the `agent.iter()` process internally, iterate until completion, and return the final `AgentRunResult`.

The `AgentRun` and `AgentRunResult` classes themselves are defined in `pydantic_ai/agent.py`. They provide the public interface for interacting with the results of the internal graph execution.

## Key Takeaways

*   **`AgentRun`**: Represents the **live, ongoing** execution of an Agent, obtained via `agent.iter()`. Allows **iteration over steps** (nodes) for real-time observation.
*   **`AgentRunResult`**: Represents the **final, completed outcome** of an Agent run, returned by `agent.run()`/`run_sync()` or available via `agent_run.result` after iteration. Contains the final **data**, **usage** stats, and **message history**.
*   Use `AgentRun` (with `agent.iter()`) when you need to see the process unfold step-by-step.
*   Use `AgentRunResult` (from `agent.run()` or `agent.run_sync()`) when you primarily need the final output and summary information.

## Conclusion

You've now learned how `pydantic-ai` represents the execution of an Agent, both as an ongoing process (`AgentRun`) and as a final outcome (`AgentRunResult`). This allows you to either observe the Agent's "thoughts" step-by-step or simply grab the final result and associated metadata like conversation history and resource consumption.

Speaking of resource consumption, the `AgentRunResult` gives us access to detailed usage statistics. How are these stats tracked, and what information do they contain? In the next chapter, we'll dive into the [**Usage**](08_usage.md) object.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
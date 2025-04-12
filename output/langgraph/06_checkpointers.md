# Chapter 6: Checkpointers

In [Chapter 5: ToolNode / tools_condition](05_toolnode___tools_condition.md), we explored how to easily integrate tools into our LangGraph applications. Our graphs are getting more complex and potentially long-running!

But what happens if you're running a complex graph that takes many steps, and your computer crashes? Or what if you want to run the first few steps, pause, and then resume later? Or maybe you want to run a graph for one user, stop, and then run a completely different graph for another user, keeping their states separate?

This is where **Checkpointers** come in.

## What's the Problem?

Imagine playing a long video game. You wouldn't want to start from the very beginning every time you play! You need a way to **save your progress**. Similarly, in complex workflows:

*   **Long-running tasks:** An AI agent might need hours to complete a research task. If it gets interrupted, starting over would be frustrating and wasteful.
*   **Interactive sessions:** A chatbot needs to remember your conversation history not just during one interaction, but potentially across days or weeks.
*   **Multiple users/sessions:** If your LangGraph application serves multiple users, you need to keep each user's state separate and be able to load the correct state when they return.

Without a way to save and load the graph's state, our applications would be ephemeral, losing all progress once the program stops.

## What is a Checkpointer?

A **Checkpointer** in LangGraph is a mechanism for automatically **saving** and **loading** the graph's internal state at different points during its execution.

Think of it exactly like:

*   **Saving your progress** in a video game.
*   **Bookmarking a page** in a long document.
*   Creating a **restore point** on your computer.

It allows your workflow to be **paused** and **resumed** later, even across different program runs or even different machines (depending on the type of checkpointer used). Checkpointers provide **persistence** for your graph's state.

**Analogy:** Imagine your graph's state ([Chapter 1: State Schema](01_state_schema.md)) is a shared whiteboard where nodes write their results. A checkpointer is like someone taking a **photograph** of the whiteboard after each important step. If the whiteboard gets erased, you can always look at the latest photograph to restore it exactly as it was.

## How to Use Checkpointers

Enabling checkpointing is surprisingly simple! You just need to pass a checkpointer object when you **compile** your graph.

LangGraph comes with several built-in checkpointers. The simplest one, perfect for getting started and testing, is the `InMemorySaver`.

Let's build a very simple graph and add an `InMemorySaver`:

```python
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
# Import the InMemorySaver
from langgraph.checkpoint.memory import InMemorySaver

# 1. Define the state
class CounterState(TypedDict):
    count: Annotated[int, operator.add] # Use add as a reducer

# 2. Define the graph
workflow = StateGraph(CounterState)

def increment(state: CounterState):
    print(f"--- Incrementing: current count {state['count']} ---")
    return {"count": 1} # Always adds 1 due to the reducer

workflow.add_node("inc", increment)
workflow.add_edge(START, "inc")
workflow.add_edge("inc", END)

# 3. Create the checkpointer instance
# This checkpointer stores state in memory
memory = InMemorySaver()

# 4. Compile the graph, passing the checkpointer
# This tells the graph to save its state using 'memory'
print("Compiling graph with checkpointer...")
app = workflow.compile(checkpointer=memory)
print("Graph compiled!")

# 5. Run the graph - requires a configuration with 'thread_id'
# Checkpointers need a unique ID for each independent run history.
# 'thread_id' is the standard way to provide this.
config = {"configurable": {"thread_id": "user-123"}}

print("\n--- First Run ---")
initial_state = {"count": 0}
final_state = app.invoke(initial_state, config=config)
print("Final state after first run:", final_state)

print("\n--- Second Run (Resuming) ---")
# No initial state needed! The checkpointer loads the last state for "user-123".
# The graph will resume from where it left off (which was the END).
# Since it ended, invoking again starts a *new* run from the last saved state.
# In this simple graph, it just runs 'inc' again.
final_state_resumed = app.invoke(None, config=config)
print("Final state after second run:", final_state_resumed)

# Expected Output:
# Compiling graph with checkpointer...
# Graph compiled!
#
# --- First Run ---
# --- Incrementing: current count 0 ---
# Final state after first run: {'count': 1}
#
# --- Second Run (Resuming) ---
# --- Incrementing: current count 1 ---
# Final state after second run: {'count': 2}
```

**Key things to notice:**

1.  **`InMemorySaver()`:** We created an instance of the simplest checkpointer.
2.  **`app = workflow.compile(checkpointer=memory)`:** We passed the checkpointer to the `compile` method. This activates the automatic saving/loading.
3.  **`config = {"configurable": {"thread_id": "user-123"}}`:** When using a checkpointer, you **must** provide a configuration dictionary (`config`) with a `configurable` key, which itself is a dictionary containing a unique `thread_id`. This ID tells the checkpointer *which conversation or run history* to save or load. Think of it as the name of your save file in a video game.
4.  **Resuming:** In the second `app.invoke(None, config=config)`, we didn't provide `initial_state`. LangGraph automatically used the checkpointer to load the last known state for `thread_id: "user-123"` (which was `{'count': 1}`) and continued execution.

That's it! By adding just those few lines, our graph now has memory.

## Types of Checkpointers

`InMemorySaver` is great for testing, but since it stores everything in memory, the state is lost when your program exits. For true persistence, LangGraph offers other checkpointer backends:

*   **`SqliteSaver`:** Stores checkpoints in a local SQLite database file. Good for single-process applications that need persistence between runs on the same machine.
    ```python
    # Example initialization (usually use a context manager)
    import sqlite3
    from langgraph.checkpoint.sqlite import SqliteSaver

    # Creates or connects to 'my_checkpoints.sqlite' file
    conn = sqlite3.connect("my_checkpoints.sqlite", check_same_thread=False)
    sqlite_saver = SqliteSaver(conn=conn)

    # Then use it in compile: app = workflow.compile(checkpointer=sqlite_saver)
    # Remember to close the connection: conn.close()
    # Or better: use SqliteSaver.from_conn_string("my_checkpoints.sqlite") context manager
    ```

*   **`PostgresSaver`:** Stores checkpoints in a PostgreSQL database. Suitable for more robust, potentially multi-process or distributed applications needing a shared, persistent state store. Requires a running Postgres server.
    ```python
    # Example initialization (usually use a context manager)
    # Needs psycopg2 installed: pip install psycopg2-binary
    from langgraph.checkpoint.postgres import PostgresSaver

    # Assumes Postgres is running and accessible via this connection string
    DB_URI = "postgresql://user:password@host:port/dbname"
    # postgres_saver = PostgresSaver.from_conn_string(DB_URI) # Use within a 'with' block

    # Then use it in compile:
    # with PostgresSaver.from_conn_string(DB_URI) as postgres_saver:
    #    postgres_saver.setup() # Create tables if they don't exist
    #    app = workflow.compile(checkpointer=postgres_saver)
    #    # ... run the app
    ```

The specific setup for SQLite and Postgres involves handling database connections, but the way you *integrate* them into your LangGraph application (`workflow.compile(checkpointer=...)`) remains the same. You just swap out the checkpointer instance.

## Under the Hood: How Checkpointing Works

When you use a checkpointer, the [Pregel Execution Engine](04_pregel_execution_engine.md) interacts with it automatically during the run.

1.  **Load State (Start/Resume):** When you call `invoke` or `stream` with a `config` containing a `thread_id`:
    *   The Pregel engine asks the checkpointer for the *latest* saved state associated with that `thread_id` (using `checkpointer.get_tuple(config)`).
    *   If a saved state exists, the checkpointer loads it from its backend (memory, file, database).
    *   The Pregel engine initializes its internal state with the loaded checkpoint. If no state exists, it starts fresh (or uses the provided input).
2.  **Save State (After Step):** After each step of the graph successfully completes (meaning one or more nodes ran, and their updates were applied to the state):
    *   The Pregel engine creates a new checkpoint representing the current state.
    *   It asks the checkpointer to **save** this new checkpoint, associating it with the current `thread_id` and a new, unique checkpoint ID (using `checkpointer.put(config, checkpoint, metadata, new_versions)`).
    *   The checkpointer writes the checkpoint data to its backend.
3.  **Continue:** The Pregel engine proceeds to the next step of the graph.

Here's a simplified sequence diagram for saving:

```mermaid
sequenceDiagram
    participant Pregel as Pregel Engine
    participant State
    participant NodeA as Node A
    participant Checkpointer

    Note over Pregel, State: Current State (Checkpoint N)
    Pregel->>NodeA: Execute Node A
    NodeA-->>Pregel: Return updates
    Pregel->>State: Apply updates using Schema
    Note over Pregel, State: New State (Ready for Checkpoint N+1)
    Pregel->>Checkpointer: Put Checkpoint N+1 (State, Config, Metadata)
    Checkpointer->>Checkpointer: Serialize state data
    Checkpointer->>Backend: Save serialized data (Memory/DB/File)
    Checkpointer-->>Pregel: Confirm save (returns new config with Checkpoint N+1 ID)
    Pregel->>Pregel: Proceed to next graph step
```

And for loading/resuming:

```mermaid
sequenceDiagram
    participant User
    participant Pregel as Pregel Engine
    participant Checkpointer
    participant Backend

    User->>Pregel: Invoke graph with Config (includes thread_id)
    Pregel->>Checkpointer: Get latest Checkpoint for thread_id
    Checkpointer->>Backend: Query for latest Checkpoint data
    Backend-->>Checkpointer: Return serialized data
    Checkpointer->>Checkpointer: Deserialize state data
    Checkpointer-->>Pregel: Return Checkpoint Tuple (State, Config, Metadata)
    Pregel->>Pregel: Initialize internal state with loaded Checkpoint
    Pregel->>Pregel: Determine next step based on loaded state
    Pregel->>NextNode: Execute next node in graph
```

The core logic happens within the `Pregel` execution loop (`langgraph/pregel/__init__.py`) which calls methods on the checkpointer object (defined by `BaseCheckpointSaver` in `langgraph/checkpoint/base/__init__.py`). The specific `put` and `get_tuple` implementations in classes like `InMemorySaver` (`langgraph/checkpoint/memory/__init__.py`), `SqliteSaver` (`langgraph/checkpoint/sqlite/__init__.py`), and `PostgresSaver` (`langgraph/checkpoint/postgres/__init__.py`) handle the interaction with the storage backend.

## Conclusion

**Checkpointers** are the key to making your LangGraph applications persistent. They automatically save the graph's state, allowing you to:

*   **Resume** interrupted workflows.
*   Maintain state across **multiple sessions**.
*   Handle **multiple users** by using distinct `thread_id`s.

Adding checkpointing is as simple as creating a checkpointer instance (like `InMemorySaver`, `SqliteSaver`, or `PostgresSaver`) and passing it to `workflow.compile()`. Remember to provide a unique `thread_id` in the `config` when invoking a checkpointed graph!

Now that we know how to build, run, and persist our graphs, let's look at how we can interact with them programmatically using client libraries. In the next chapter, we'll explore the [LangGraph SDK (Python/JS Clients)](07_langgraph_sdk__python_js_clients_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
# Tutorial: pf1

This project acts like an automatic **report writer** for YouTube videos.
You give it a *YouTube video link*, and it watches the video (by reading its *transcript*) to understand the main points.
It uses **Artificial Intelligence (AI)** to identify key *topics*, create simple **question & answer pairs** about them, and even write an **"Explain Like I'm 5"** summary for each topic.
Finally, it neatly organizes all this information into a web page (**HTML report**) for easy reading.


**Source Repository:** [https://github.com/Kjdragan/pf1](https://github.com/Kjdragan/pf1)

```mermaid
flowchart TD
    A0["Pipeline Orchestration"]
    A1["Node (Pipeline Step)"]
    A2["Shared Memory"]
    A3["Topic Processing Orchestrator"]
    A4["LLM Utility"]
    A5["YouTube Data Utilities"]
    A6["HTML Generation"]
    A7["Logging"]
    A0 -- "Executes Nodes" --> A1
    A0 -- "Initializes & Passes Data via" --> A2
    A0 -- "Calls Specific Node" --> A3
    A1 -- "Reads/Writes Data" --> A2
    A1 -- "Uses for AI Tasks" --> A4
    A1 -- "Uses for Video Data" --> A5
    A1 -- "Uses for Report Creation" --> A6
    A3 -- "Manages Worker Nodes" --> A1
    A0 -- "Uses for Overall Logging" --> A7
```

## Chapters

1. [Pipeline Orchestration](01_pipeline_orchestration.md)
2. [Node (Pipeline Step)](02_node__pipeline_step_.md)
3. [Shared Memory](03_shared_memory.md)
4. [Topic Processing Orchestrator](04_topic_processing_orchestrator.md)
5. [YouTube Data Utilities](05_youtube_data_utilities.md)
6. [LLM Utility](06_llm_utility.md)
7. [HTML Generation](07_html_generation.md)
8. [Logging](08_logging.md)


---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
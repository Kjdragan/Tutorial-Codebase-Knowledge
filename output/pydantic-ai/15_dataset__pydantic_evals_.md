# Chapter 15: Dataset (pydantic-evals) - Your AI's Exam Questions

In [Chapter 14: State Persistence (pydantic-graph)](14_state_persistence__pydantic_graph_.md), we explored how `pydantic-graph` can save and load the progress of your Agent's internal workflow, like saving a game. This is great for managing complex or long-running tasks.

But once you've built your [Agent](01_agent.md) – maybe one that understands time ranges, extracts information, or answers questions – how do you know if it's actually *good*? Does it consistently give the right answers? Does it handle tricky edge cases? Simply running it a few times isn't enough to be sure. We need a systematic way to test or *evaluate* it.

This brings us to a new part of the Pydantic ecosystem: **`pydantic-evals`**. This library helps you rigorously evaluate your AI applications. The first step in evaluation is defining *what* you want to test. That's where the `Dataset` comes in.

## What's the Big Idea? Exam Questions for Your AI

Imagine your [Agent](01_agent.md) is a student learning a new skill, like understanding dates and times. How do you check if the student has learned well? You give them an exam!

A `pydantic-evals` **`Dataset`** is exactly like that exam. It's a collection of **test cases** designed to check how well your Agent (or any function you want to test) performs on different scenarios.

Each individual "exam question" in the dataset is represented by a **`Case`** object. A `Case` typically includes:

1.  **Inputs:** The specific question or data you give to the Agent (e.g., "What time is it in London next Tuesday afternoon?").
2.  **Expected Output (Optional):** The correct answer you hope the Agent will produce (e.g., a specific time range object). This isn't always needed, but it's useful for checking correctness.
3.  **Metadata (Optional):** Extra information about the test case (e.g., "This tests handling of relative dates").
4.  **Evaluators (Optional):** Specific rules or criteria for judging the Agent's answer *for this particular case*. We'll cover [Evaluators](16_evaluator__pydantic_evals_.md) in the next chapter.

So, a `Dataset` bundles together many `Case` objects, creating a comprehensive test suite for your AI "student".

## Why Do We Need Datasets?

*   **Consistency:** Ensure your Agent performs well across many different inputs, not just the few you tested manually.
*   **Regression Testing:** Check if changes you make to your Agent break its previous behavior on known cases.
*   **Comparing Models/Prompts:** Run the same dataset against different versions of your Agent (e.g., using GPT-3.5 vs. GPT-4o, or with different prompts) to see which performs better.
*   **Clarity:** Clearly define what "good performance" means for your specific task.

## Creating Your First `Case`

Let's make a single test case (an exam question) for an imaginary Agent that converts text to uppercase.

```python
# Requires: pip install pydantic-evals
from pydantic_evals import Case

# Define a single test case
simple_case = Case(
    name='Simple Hello', # A descriptive name for this test
    inputs={'text': 'Hello World'}, # What we give the Agent
    expected_output='HELLO WORLD' # What we hope the Agent outputs
)

print(simple_case)
```

**Explanation:**
*   We import `Case` from `pydantic_evals`.
*   We create an instance of `Case`.
    *   `name`: A helpful identifier for this specific test.
    *   `inputs`: A dictionary containing the input for our uppercase Agent. (The structure of `inputs` depends on what your Agent expects).
    *   `expected_output`: The exact string we expect the Agent to return for these inputs.

This `simple_case` object now represents one scenario we want to test our Agent against.

## Building a `Dataset`

A single case isn't very useful; we need a collection. Let's create a `Dataset` with a couple of cases for our uppercase Agent.

```python
from pydantic_evals import Case, Dataset

# Create multiple cases
case1 = Case(name='Simple Hello', inputs={'text': 'Hello World'}, expected_output='HELLO WORLD')
case2 = Case(name='With Numbers', inputs={'text': 'Test 123'}, expected_output='TEST 123')
case3 = Case(name='Empty String', inputs={'text': ''}, expected_output='')

# Create a Dataset containing these cases
uppercase_dataset = Dataset(
    cases=[case1, case2, case3]
    # We could add dataset-wide evaluators here later
)

print(f"Dataset created with {len(uppercase_dataset.cases)} cases.")
```

**Explanation:**
*   We import `Dataset`.
*   We create several `Case` objects as before.
*   We create a `Dataset` instance, passing our list of `Case` objects to the `cases` argument.
*   Now, `uppercase_dataset` holds our entire "exam" for the uppercase Agent.

## Saving Your Dataset: Making it Reusable

Typing out cases in Python code is fine for small examples, but for real evaluations, you'll want to save your dataset to a file so you can easily load and reuse it, or share it with others. `pydantic-evals` supports saving to JSON or YAML format. YAML is often preferred because it's easier for humans to read and edit.

```python
from pathlib import Path

# Define the path where we want to save the dataset
save_path = Path("uppercase_test_set.yaml")

# Save the dataset to the YAML file
uppercase_dataset.to_file(save_path, fmt='yaml')

print(f"Dataset saved to: {save_path.absolute()}")
```

**Explanation:**
*   We import `Path` from `pathlib` to handle file paths easily.
*   We create a `Path` object representing `uppercase_test_set.yaml`.
*   We call the `to_file()` method on our `uppercase_dataset`.
    *   The first argument is the path.
    *   `fmt='yaml'` tells it to save in YAML format.

If you open `uppercase_test_set.yaml` after running this, you'll see something like:

```yaml
# yaml-language-server: $schema=uppercase_test_set_schema.json
cases:
- name: Simple Hello
  inputs:
    text: Hello World
  expected_output: HELLO WORLD
- name: With Numbers
  inputs:
    text: Test 123
  expected_output: TEST 123
- name: Empty String
  inputs:
    text: ''
  expected_output: ''
```
*(Note: The `# yaml-language-server...` line is automatically added to help code editors understand the file structure.)*

This file clearly shows our test cases in a human-readable format.

## Loading Your Dataset

Now that we have a saved file, we can easily load it back into a `Dataset` object anytime.

```python
from pydantic_evals import Dataset
from pathlib import Path

# Path to the saved file
load_path = Path("uppercase_test_set.yaml")

# Define the expected types for this dataset
# (This helps pydantic-evals parse the file correctly)
# For our simple example: inputs are dict, output is str, metadata is None
LoadedDatasetType = Dataset[dict, str, None]

# Load the dataset from the file
loaded_dataset = LoadedDatasetType.from_file(load_path, fmt='yaml')

print(f"Dataset loaded with {len(loaded_dataset.cases)} cases.")
print(f"First case inputs: {loaded_dataset.cases[0].inputs}")
```

**Explanation:**
*   We define the path `load_path`.
*   **Type Hinting:** We create `LoadedDatasetType = Dataset[dict, str, None]`. This tells `pydantic-evals` what Python types to expect for the `inputs`, `expected_output`, and `metadata` fields within the YAML file. This is important for correctly parsing the loaded data. Replace `dict`, `str`, `None` with the actual types used in your specific dataset (e.g., `MyInputModel`, `MyOutputModel`, `MyMetadataModel`).
*   We call the class method `LoadedDatasetType.from_file()`, passing the path and format.
*   This returns a new `Dataset` object populated with the data from the file.

Now `loaded_dataset` is ready to be used for evaluating our uppercase Agent!

## Generating Datasets Automatically (Advanced Peek)

Manually creating large datasets can be tedious. `pydantic-evals` includes a helper function, `generate_dataset` (which uses `pydantic-ai` itself!), to ask an LLM to generate test cases for you based on instructions and type definitions.

```python
# This is a conceptual example - see full example code for details
# from pydantic_evals.generation import generate_dataset
# from pydantic_evals import Dataset
#
# # Define expected input/output types (e.g., using Pydantic models)
# class MyInputs(BaseModel): ...
# class MyOutput(BaseModel): ...
#
# async def generate():
#     # Ask an LLM to generate 5 cases matching these types
#     generated_dataset = await generate_dataset(
#         dataset_type=Dataset[MyInputs, MyOutput, None],
#         model='openai:gpt-4o', # Use a capable model
#         n_examples=5,
#         extra_instructions="Generate diverse test cases..."
#     )
#     generated_dataset.to_file("generated_dataset.yaml")
```
This can be a powerful way to bootstrap your evaluation efforts, though you'll likely want to review and refine the generated cases. You can see a practical example in `examples/pydantic_ai_examples/evals/example_01_generate_dataset.py`.

## Under the Hood: Pydantic Models

How does `pydantic-evals` handle the saving and loading, especially with complex types? Internally, `Dataset` and `Case` rely heavily on Pydantic models for structure and validation.

When you call `dataset.to_file()`, `pydantic-evals`:
1.  Converts your `Dataset` object (containing `Case` objects and `Evaluator` instances) into an internal Pydantic model representation (like `_DatasetModel` and `_CaseModel` mentioned in the `pydantic_evals/dataset.py` code).
2.  Uses Pydantic's serialization features to dump this internal model to JSON or YAML, handling complex types correctly.
3.  It can also generate a JSON Schema definition for your specific dataset structure, which helps with validation and editor tooling (that's where the `$schema` line in the YAML comes from).

When you call `Dataset.from_file()`:
1.  It reads the YAML or JSON file.
2.  It uses the corresponding internal Pydantic model (`_DatasetModel` specialized with your types like `Dataset[dict, str, None]`) to parse and validate the raw data from the file.
3.  It converts the validated internal model back into the user-facing `Dataset` and `Case` objects.

This use of Pydantic makes the serialization robust and type-safe.

## Key Takeaways

*   A `pydantic-evals` **`Dataset`** is a collection of test cases used to evaluate an AI Agent or function.
*   It's like an **exam** for your AI.
*   Each test case is a **`Case`** object, containing `inputs`, and optional `expected_output`, `metadata`, and case-specific `evaluators`.
*   Datasets help ensure **consistency**, enable **regression testing**, and allow **comparison** between different AI versions or models.
*   You can easily **save** datasets to YAML or JSON files (`dataset.to_file()`) and **load** them back (`Dataset.from_file()`).
*   Providing correct type hints (e.g., `Dataset[MyInputs, MyOutputs, MyMetadata]`) is important when loading datasets.

## Conclusion

You've now learned about the foundational element for evaluating your AI applications with `pydantic-evals`: the `Dataset`. By defining a structured set of test cases (`Case` objects), you create a reusable "exam" to systematically measure your Agent's performance. Saving and loading these datasets makes the evaluation process repeatable and shareable.

But how do we actually *judge* the Agent's answers against the dataset? Just having inputs and expected outputs isn't enough. We need rules and criteria for scoring. In the next chapter, we'll dive into the components that perform this judgment: [**Evaluator (pydantic-evals)**](16_evaluator__pydantic_evals_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)
# Import the necessary class from the ADK
from google.adk.agents import LlmAgent

# Create our first Agent instance
greeting_agent = LlmAgent(
    name="Greeter",
    description="Politely greets the user.",
    # Tell the LLM *how* to act
    instruction="You are a friendly assistant. Greet the user warmly.",
    # Specify which LLM to use (we'll cover models more later)
    model="gemini-1.5-flash"
)

# In a real application, we would now 'run' this agent.
# We'll learn how to do that in the next chapter!
print(f"Created Agent named: {greeting_agent.name}")

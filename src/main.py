import json
import logging
from agent import Agent
from client_tool import ClientTool
from tools.math import sum_numbers, multiply_numbers, subtract_numbers, divide_numbers, power, square_root

# Configure logging so INFO logs are visible
logging.basicConfig(level=logging.INFO, format="%(message)s")
# Suppress verbose logs from third-party clients
logging.getLogger("httpx").setLevel(logging.WARNING)

# Create a list of ClientTool objects
tools = [
    ClientTool("add", "Add two numbers and return the sum.", sum_numbers),
    ClientTool("multiply", "Multiply two numbers and return the product.", multiply_numbers),
    ClientTool("subtract", "Subtract the second number from the first.", subtract_numbers),
    ClientTool("divide", "Divide the first number by the second.", divide_numbers),
    ClientTool("power", "Raise the base to the power of the exponent.", power),
    ClientTool("sqrt", "Calculate the square root of a number.", square_root)
]

# Initialize the agent with the tools
agent = Agent(
    name="math_assistant",
    system_prompt=(
        "You are a helpful math assistant. "
        "Always use the available tools to perform calculations accurately."
    ),
    tools=tools
)

# Initialize conversation with user message
context = [
    {
        "role": "user",
        "content": "Solve this equation: 2x² - 7x + 3 = 0"
    }
]

# Send message to the stateless agent
result = agent.run(context)

# Display the response
print("\nFinal response:")
print(result.final_output)

# Show the conversation history
print("\nConversation history:")
print(json.dumps(result.history, indent=2))
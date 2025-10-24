import json
import logging
from openai import OpenAI
from client_tool import ClientTool

# Logger for the agent
logger = logging.getLogger(__name__)


class AgentRunResult:
    def __init__(self, final_output, history):
        self.final_output = final_output
        self.history = history


class Agent:
    # Base system prompt to be used for all agents
    BASE_SYSTEM_PROMPT = (
        "You are an autonomous agent that can take multiple tool-calling steps. "
        "When tools are available, prefer calling them to compute, fetch, or transform information "
        "rather than fabricating results. "
    )

    def __init__(
        self,
        name,
        system_prompt="You are a helpful assistant.",
        model="gpt-5",
        tools=None,
        max_turns=10,
        reasoning_effort="low"
    ):
        self.client = OpenAI()
        self.name = name
        self.model = model
        self.system_prompt = self.BASE_SYSTEM_PROMPT + system_prompt
        self.max_turns = max_turns
        self.reasoning_effort = reasoning_effort

        # Expect a list of Tool objects
        if tools is None:
            tools = []

        # Validate tools are ClientTool instances
        for t in tools:
            if not isinstance(t, ClientTool):
                raise TypeError("Tools must be a list of ClientTool instances")

        # Map tool names to ClientTool objects and collect schemas
        self.tools = {t.name: t for t in tools}
        self.tool_schemas = [t.schema for t in tools]

    def call_tool(self, function_call):
        # Get the function name, arguments, and call ID
        tool_name = function_call.name
        call_id = function_call.call_id
        
        # Parse arguments from JSON string to Python dict
        tool_input = json.loads(function_call.arguments)

        # Log which tool is being called
        logger.info(f"🔧 [{self.name}] called tool: {tool_name}({tool_input})")
        
        try:
            # Execute via ClientTool.execute
            result = self.tools[tool_name].execute(**tool_input)
        except KeyError:
            # Return an error message if the tool is not found
            result = f"Error: Tool {tool_name} not found"
        except Exception as e:
            # Return an error message if the tool fails
            result = f"Error: {str(e)}"

        # Return the tool result in GPT-5 Responses API format
        return {
            "type": "function_call_output",
            "call_id": call_id,
            "output": json.dumps({"result": result})
        }

    def run(self, input):
        # Create a copy of the input list to avoid modifying the original
        context = input.copy()

        # Initialize turn counter to track iterations
        turn = 0

        # Loop until the model returns a final answer or the max turns is reached
        while turn < self.max_turns:
            # Increment the turn
            turn += 1

            # Ask the model for a response
            response = self.client.responses.create(
                model=self.model,
                instructions=self.system_prompt,
                input=context,
                tools=self.tool_schemas,
                reasoning={"effort": self.reasoning_effort} if self.model.startswith("gpt-5") else None,
                store=False
            )

            # Check if model wants to use any tools by looking for function_calls in output
            function_calls = [
                item for item in response.output
                if item.type == "function_call"
            ]

            if function_calls:
                # Execute each function call
                function_outputs = []
                
                # First, add the function calls to the context
                for function_call in function_calls:
                    context.append({
                        "type": "function_call",
                        "name": function_call.name,
                        "arguments": function_call.arguments,
                        "call_id": function_call.call_id
                    })
                
                # Then execute and collect the outputs
                for function_call in function_calls:
                    # Execute the tool with the given input
                    tool_result = self.call_tool(function_call)
                    # Add result to function outputs list
                    function_outputs.append(tool_result)

                # Add all function outputs to the context
                context.extend(function_outputs)
        
            else:
                # Add the final response to the context
                context.append({
                    "role": "assistant",
                    "content": response.output_text
                })
                
                # Return the agent history and final output
                return AgentRunResult(final_output=response.output_text, history=context)

        # If the max turns is reached, raise an exception
        raise Exception("Max turns reached")
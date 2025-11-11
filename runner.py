import os
import json
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv
from agent_tools import AgentTools
load_dotenv()

class LLMAgent:
    """
    LLM-powered agent with system prompt.
    """

    def __init__(self): 
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("GROQ_MODEL")
        if not api_key and model:
            raise ValueError("GROQ_API_KEY or model not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.tools = AgentTools()
        self.model = model
        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for general information, news, current events, and how-to guides.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The web search query."},
                            "max_results": {"type": "integer", "description": "Max results.", "default": 5}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "research_paper_search",
                    "description": "Search academic research papers on arXiv for scientific or technical topics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Research topic or keywords."},
                            "max_results": {"type": "integer", "description": "Max papers.", "default": 5}
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def _execute_tool(self, tool_name: str, tool_input: Dict) -> List[Dict]:
        """Execute tool with validation."""
        tool_methods = {
            "web_search": self.tools.web_search,
            "research_paper_search": self.tools.research_paper_search
        }
        
        if tool_name not in tool_methods:
            return [{"error": f"Unknown tool: {tool_name}"}]

        query = tool_input.get("query")
        if not query:
            return [{"error": f"Missing 'query' parameter for tool: {tool_name}"}]
            
        
        try:
            max_results = int(tool_input.get("max_results", 5))
        except (ValueError, TypeError):
            max_results = 5

        return tool_methods[tool_name](
            query=query,
            max_results=max_results
        )

    def _get_llm_response(self, messages: List[Dict], use_tools: bool = True) -> str:
        """Get response from LLM with optional tool use."""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.0
        }
        
        if use_tools:
            kwargs.update({
                "tools": self.tool_definitions,
                "tool_choice": "auto"
            })
            
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message

    def run(self, user_query: str) -> str:
        """
        Execute the agent with improved logic via a stronger system prompt.
        """
        if not user_query or not user_query.strip():
            return "Please provide a valid query."
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. You have access to tools. "
                    "Your primary goal is to provide accurate, up-to-date answers. "
                    
                    "**Rule 1: Always prefer to use a tool if the query is about facts, "
                    "people, places, news, or specific knowledge (e.g., 'who is the prime minister?', "
                    "'weather in Jaipur').** "
                    
                    "**Rule 2: Only answer directly if the query is small talk (e.g., 'hello'), "
                    "a simple command (e.g., 'thank you'), or a question **about you or your tools** "
                    "(e.g., 'what tools do you have?', 'what are your capabilities?').** "
                    
                    "Use 'web_search' for general facts, news, and current events. "
                    "Use 'research_paper_search' for academic or scientific topics."\
                    "Use 'research_paper_search' if you need detailed scientific information. "
                    "If you are unsure which tool should i use, prefer using 'research_paper_search' over answering directly."
                )

            },
            {"role": "user", "content": user_query}
        ]


        # 1. Get initial response (LLM decides to use tools or answer directly)
        response_message = self._get_llm_response(messages, use_tools=True)
        
        # 2. Check if the LLM decided to call a tool
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            messages.append(response_message)
            
            tool_notifications = [] 
            
            # 3. Execute all requested tools
            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                query = tool_input.get('query', 'N/A')

                if tool_name == "web_search":
                    tool_notifications.append(f"Using the web_search tool for: '{query}'")
                elif tool_name == "research_paper_search":
                    tool_notifications.append(f"Using the research_paper_search tool on: '{query}'")

                tool_results = self._execute_tool(tool_name, tool_input)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_results)
                })
            
            final_response = self._get_llm_response(messages, use_tools=False)

            print(tool_notifications,"Notification Header")
            notification_header = "\n".join(tool_notifications)
            return f"**[Tools Activated]**\n{notification_header}\n\n---\n\n{final_response.content}"
        
        return response_message.content

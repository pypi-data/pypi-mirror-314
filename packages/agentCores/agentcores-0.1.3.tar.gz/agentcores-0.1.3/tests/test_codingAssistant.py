# tests/test_coding_assistant.py
import unittest
from unittest.mock import patch, MagicMock
import json
import sys
from pathlib import Path

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from agentCores import agentCore

@unittest.skipIf(not OLLAMA_AVAILABLE, "Ollama package not installed")
class TestCodingAssistant(unittest.TestCase):
    def setUp(self):
        self.core = agentCore()
        # Define the exact coding assistant configuration from the example
        self.coding_config = {
            "agent_id": "coding_assistant",
            "models": {
                "large_language_model": "codellama",
                "embedding_model": "nomic-embed-text"
            },
            "prompts": {
                "user_input_prompt": "You are an expert programming assistant. Focus on writing clean, efficient, and well-documented code. Explain your implementation choices and suggest best practices.",
                "agentPrompts": {
                    "llmSystemPrompt": "When analyzing code or programming problems, start by understanding the requirements, then break down the solution into logical steps. Include error handling and edge cases.",
                    "llmBoosterPrompt": "Enhance your responses with: 1) Performance considerations 2) Common pitfalls to avoid 3) Testing strategies 4) Alternative approaches when relevant."
                }
            },
            "commandFlags": {
                "STREAM_FLAG": True,
                "LOCAL_MODEL": True,
                "CODE_MODE": True
            },
            "databases": {
                "conversation_history": "coding_assistant_chat.db",
                "python_knowledge": "pythonKnowledge.db",
                "code_examples": "code_snippets.db"
            }
        }

    def test_coding_assistant_creation(self):
        """Test creation of coding assistant with the exact configuration"""
        coding_agent = self.core.mintAgent(
            agent_id=self.coding_config["agent_id"],
            model_config=self.coding_config["models"],
            prompt_config=self.coding_config["prompts"],
            command_flags=self.coding_config["commandFlags"],
            db_config=self.coding_config["databases"]
        )

        # Verify all configuration aspects
        self.assertEqual(coding_agent["agentCore"]["agent_id"], "coding_assistant")
        self.assertEqual(coding_agent["agentCore"]["models"]["large_language_model"], "codellama")
        self.assertEqual(coding_agent["agentCore"]["models"]["embedding_model"], "nomic-embed-text")
        
        # Verify prompts
        self.assertEqual(
            coding_agent["agentCore"]["prompts"]["user_input_prompt"],
            self.coding_config["prompts"]["user_input_prompt"]
        )
        self.assertEqual(
            coding_agent["agentCore"]["prompts"]["agentPrompts"]["llmSystemPrompt"],
            self.coding_config["prompts"]["agentPrompts"]["llmSystemPrompt"]
        )
        
        # Verify command flags
        self.assertTrue(coding_agent["agentCore"]["commandFlags"]["CODE_MODE"])
        self.assertTrue(coding_agent["agentCore"]["commandFlags"]["STREAM_FLAG"])
        self.assertTrue(coding_agent["agentCore"]["commandFlags"]["LOCAL_MODEL"])
        
        # Verify database configurations
        self.assertEqual(
            coding_agent["agentCore"]["databases"]["conversation_history"],
            "coding_assistant_chat.db"
        )
        self.assertEqual(
            coding_agent["agentCore"]["databases"]["python_knowledge"],
            "pythonKnowledge.db"
        )
        self.assertEqual(
            coding_agent["agentCore"]["databases"]["code_examples"],
            "code_snippets.db"
        )

    @patch('ollama.chat')
    def test_bst_implementation(self, mock_chat):
        """Test the coding assistant's BST implementation example"""
        # Example BST implementation response
        bst_response = [
            {'message': {'content': 'class Node:\n'}},
            {'message': {'content': '    def __init__(self, value):\n'}},
            {'message': {'content': '        self.value = value\n'}},
            {'message': {'content': '        self.left = None\n'}},
            {'message': {'content': '        self.right = None\n'}},
            {'message': {'content': '\nclass BinarySearchTree:\n'}},
            {'message': {'content': '    def __init__(self):\n'}},
            {'message': {'content': '        self.root = None\n'}}
        ]
        mock_chat.return_value = bst_response

        # Create coding assistant
        coding_agent = self.core.mintAgent(
            agent_id=self.coding_config["agent_id"],
            model_config=self.coding_config["models"],
            prompt_config=self.coding_config["prompts"],
            command_flags=self.coding_config["commandFlags"],
            db_config=self.coding_config["databases"]
        )

        # Define the stream_code_chat function from the example
        def stream_code_chat(agent_config, prompt):
            system_prompt = (
                f"{agent_config['agentCore']['prompts']['user_input_prompt']} "
                f"{agent_config['agentCore']['prompts']['agentPrompts']['llmSystemPrompt']} "
                f"{agent_config['agentCore']['prompts']['agentPrompts']['llmBoosterPrompt']}"
            )
            
            stream = ollama.chat(
                model=agent_config["agentCore"]["models"]["large_language_model"],
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=True,
            )
            return stream

        # Test the BST implementation request
        response = stream_code_chat(
            coding_agent,
            "Write a Python function to implement a binary search tree with insert and search methods"
        )

        # Verify the chat call
        mock_chat.assert_called_once()
        call_args = mock_chat.call_args[1]
        
        # Verify model and streaming
        self.assertEqual(call_args['model'], 'codellama')
        self.assertTrue(call_args['stream'])
        
        # Verify message structure
        messages = call_args['messages']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[1]['role'], 'user')
        self.assertEqual(
            messages[1]['content'],
            "Write a Python function to implement a binary search tree with insert and search methods"
        )
        
        # Verify system prompt combines all prompt elements
        system_message = messages[0]['content']
        self.assertIn("expert programming assistant", system_message)
        self.assertIn("analyzing code or programming problems", system_message)
        self.assertIn("Performance considerations", system_message)

def stream_code_chat_test(agent_config, prompt):
    """Test helper function to capture streamed output"""
    output = []
    system_prompt = (
        f"{agent_config['agentCore']['prompts']['user_input_prompt']} "
        f"{agent_config['agentCore']['prompts']['agentPrompts']['llmSystemPrompt']} "
        f"{agent_config['agentCore']['prompts']['agentPrompts']['llmBoosterPrompt']}"
    )
    
    stream = ollama.chat(
        model=agent_config["agentCore"]["models"]["large_language_model"],
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        stream=True,
    )
    
    for chunk in stream:
        content = chunk['message']['content']
        output.append(content)
    return output

if __name__ == '__main__':
    unittest.main()
# tests/test_agentCore.py
import unittest
from agentCores import agentCore

class TestAgentCore(unittest.TestCase):
    def setUp(self):
        self.core = agentCore()
        
    def test_init_template(self):
        template = self.core.initTemplate()
        self.assertIsNotNone(template)
        self.assertIn("agentCore", template)
        
    def test_mint_agent(self):
        agent = self.core.mintAgent(
            agent_id="test_agent",
            model_config={"large_language_model": "test_model"},
            prompt_config={"user_input_prompt": "test prompt"}
        )
        self.assertEqual(agent["agentCore"]["agent_id"], "test_agent")
        self.assertIsNotNone(agent["agentCore"]["uid"])

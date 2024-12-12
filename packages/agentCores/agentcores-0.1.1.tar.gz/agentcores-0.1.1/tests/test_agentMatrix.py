# tests/test_agentMatrix.py
import unittest
import os
from agentCores import agentMatrix

class TestAgentMatrix(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_matrix.db"
        self.matrix = agentMatrix(self.test_db)
        
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
    def test_upsert_and_get(self):
        test_doc = '{"test": "data"}'
        self.matrix.upsert(
            documents=[test_doc],
            ids=["test_id"],
            metadatas=[{"save_date": "2024-12-11"}]
        )
        result = self.matrix.get(ids=["test_id"])
        self.assertEqual(result["documents"][0], test_doc)
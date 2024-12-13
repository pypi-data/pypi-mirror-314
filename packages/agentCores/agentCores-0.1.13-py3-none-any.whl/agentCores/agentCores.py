# agentCores.py
"""agentCores

A flexible framework for creating and managing AI agent configurations.

This package provides a comprehensive system for defining, storing, and managing
AI agent configurations. It supports custom templates, versioning, and persistent
storage of agent states and configurations.

Key Features:
1. Template-based agent creation with customization
2. SQLite-based persistent storage
3. Version control and unique identifiers for agents
4. Command-line interface for agent management
5. Support for custom database configurations
6. Flexible model and prompt management

Basic Usage:
    ```python
    from agentCores import agentCores
    
    # Create with default configuration
    agentCoresInstance = agentCores()
    
    # Create with custom database paths
    agentCoresInstance = agentCores(db_config={
        "agent_matrix": "custom_matrix.db",
        "conversation_history": "custom_conversations.db",
        "knowledge_base": "custom_knowledge.db"
    })
    
    # Create an agent with custom configuration
    agent = agentCoresInstance.mintAgent(
        agent_id="custom_agent",
        db_config={"conversation_history": "custom_agent_conv.db"},
        model_config={"large_language_model": "gpt-4"},
        prompt_config={"user_input_prompt": "Custom prompt"}
    )
    ```

Advanced Usage:
    ```python
    # Create with custom template
    custom_template = {
        "agent_id": "specialized_agent",
        "models": {
            "large_language_model": "llama",
            "custom_model": "specialized_model"
        },
        "custom_section": {
            "custom_param": "custom_value"
        }
    }
    
    agentCoresInstance = agentCores(template=custom_template)
    ```

Installation:
    pip install agentCores

Project Links:
    Homepage: https://github.com/Leoleojames1/agentCores
    Documentation: https://agentcore.readthedocs.io/ #NOT AVAILABLE
    Issues: https://github.com/Leoleojames1/agentCores/issues

Author: Leo Borcherding
Version: 0.1.0
Date: 2024-12-11
License: MIT
"""
# add uithub scrape, add arxiv
import sqlite3
import json
import os
import time
import hashlib
import copy
from pathlib import Path
from typing import Optional, Dict, Any
from pkg_resources import resource_filename
from .agentMatrix import agentMatrix

class agentCores:
    
    DEFAULT_DB_PATHS = {
        "system": {
            "agent_matrix": "system/agent_matrix.db",
            "documentation": "system/agentcore_docs.db",
            "templates": "system/agent_templates.db"
        },
        "agents": {
            "conversation": "agents/{agent_id}/conversations.db",
            "knowledge": "agents/{agent_id}/knowledge.db",
            "embeddings": "agents/{agent_id}/embeddings.db"
        },
        "shared": {
            "global_knowledge": "shared/global_knowledge.db",
            "models": "shared/model_configs.db",
            "prompts": "shared/prompt_templates.db"
        }
    }
    
    def __init__(self, 
                 db_path: str = None,
                 db_config: Optional[Dict] = None,
                 template: Optional[Dict] = None):
        """Initialize AgentCore with optional custom configuration."""
        self.current_date = time.strftime("%Y-%m-%d")
        
        # Use package data path if no custom path provided
        if db_path is None:
            db_path = resource_filename('agentCores', 'data/agent_matrix.db')
            
        self.agent_library = agentMatrix(db_path)
        
        # Initialize template with any custom configuration
        self.initTemplate(template)
        
        # Update database configuration if provided
        if db_config:
            self.base_template["agentCore"]["databases"].update(db_config)

    def _init_db_paths(self, custom_config: Optional[Dict] = None) -> Dict:
        """Initialize all database paths with optional custom configuration"""
        db_paths = copy.deepcopy(self.DEFAULT_DB_PATHS)
        
        # Apply base path to all default paths
        for category in db_paths:
            for key, path in db_paths[category].items():
                db_paths[category][key] = str(self.base_path / path)

        # Apply any custom configurations
        if custom_config:
            for category, paths in custom_config.items():
                if category in db_paths:
                    db_paths[category].update(paths)

        return db_paths
    
    def get_agent_db_paths(self, agent_id: str) -> Dict[str, str]:
        """Get all database paths for a specific agent"""
        paths = {}
        for key, path_template in self.DEFAULT_DB_PATHS["agents"].items():
            path = path_template.format(agent_id=agent_id)
            paths[key] = str(self.base_path / path)
        return paths
    
    def _init_directory_structure(self):
        """Create the directory structure for AgentCore databases"""
        for category in ["system", "agents", "shared"]:
            (self.base_path / category).mkdir(parents=True, exist_ok=True)
    
    def init_base_databases(self):
        """Initialize all system and shared databases"""
        # Create system databases
        for db_name, db_path in self.db_paths["system"].items():
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self._init_specific_db(db_name, db_path)

        # Create shared databases
        for db_name, db_path in self.db_paths["shared"].items():
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self._init_specific_db(db_name, db_path)
            
    def create_agent_databases(self, agent_id: str) -> Dict[str, str]:
        """Create all necessary databases for a new agent"""
        paths = self.get_agent_db_paths(agent_id)
        
        # Create agent directory
        agent_dir = self.base_path / f"agents/{agent_id}"
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize each database
        for db_type, db_path in paths.items():
            self._init_specific_db(db_type, db_path)
            
        return paths

    def _init_specific_db(self, db_type: str, db_path: str):
        """Initialize a specific type of database with the appropriate schema"""
        with sqlite3.connect(db_path) as conn:
            if db_type == "conversation":
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY,
                        timestamp TEXT,
                        role TEXT,
                        content TEXT,
                        session_id TEXT,
                        metadata TEXT
                    )
                """)
            elif db_type == "knowledge":
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS knowledge_base (
                        id INTEGER PRIMARY KEY,
                        topic TEXT,
                        content TEXT,
                        source TEXT,
                        last_updated TEXT
                    )
                """)
            elif db_type == "embeddings":
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS embeddings (
                        id INTEGER PRIMARY KEY,
                        text TEXT,
                        embedding BLOB,
                        metadata TEXT
                    )
                """)
                
    def initTemplate(self, custom_template: Optional[Dict] = None) -> Dict:
        """Initialize or customize the agent template while maintaining required structure."""
        # Base template structure (as shown in previous response)
        base_template = {
            "agentCore": {
                "agent_id": None,
                "version": None,
                "uid": None,
                "cpu_noise_hex": None,
                "save_state_date": None,
                "models": {
                    "large_language_model": None,
                    "embedding_model": None,
                    "language_and_vision_model": None,
                    "yolo_model": None,
                    "whisper_model": None,
                    "voice_model": None
                },
                "prompts": {
                    "user_input_prompt": "",
                    "agentPrompts": {
                        "llmSystemPrompt": None,
                        "llmBoosterPrompt": None,
                        "visionSystemPrompt": None,
                        "visionBoosterPrompt": None
                    }
                },
                "commandFlags": {
                    "TTS_FLAG": False,
                    "STT_FLAG": False,
                    "CHUNK_FLAG": False,
                    "AUTO_SPEECH_FLAG": False,
                    "LLAVA_FLAG": False,
                    "SPLICE_FLAG": False,
                    "SCREEN_SHOT_FLAG": False,
                    "LATEX_FLAG": False,
                    "CMD_RUN_FLAG": False,
                    "AGENT_FLAG": True,
                    "MEMORY_CLEAR_FLAG": False
                },
                "conversation": {
                    "save_name": "defaultConversation",
                    "load_name": "defaultConversation",
                    "conversation_history": "defaultConversation"
                },
                "databases": {
                    "agent_matrix": "agent_matrix.db",
                    "conversation_history": "{agent_id}_conversation.db",
                    "knowledge_base": "knowledgeBase.db"
                }
            }
        }
        
        if custom_template:
            def deep_merge(base: Dict, custom: Dict) -> Dict:
                for key, value in custom.items():
                    if isinstance(base.get(key), dict) and isinstance(value, dict):
                        deep_merge(base[key], value)
                    else:
                        base[key] = value
                return base
            
            if "agentCore" not in custom_template:
                custom_template = {"agentCore": custom_template}
            
            deep_merge(base_template["agentCore"], custom_template["agentCore"])
        
        self.base_template = base_template
        self.agentCores = json.loads(json.dumps(base_template))
        return base_template

    def getNewAgentCore(self) -> Dict:
        """Get a fresh agent core based on the base template."""
        return json.loads(json.dumps(self.base_template))  # Deep copy
        
    def _createAgentConfig(self, agent_id: str, config: Dict) -> Dict:
        """Create a full agent configuration from base template and config data."""
        new_core = self.getNewAgentCore()
        new_core["agentCore"]["agent_id"] = agent_id
        new_core["agentCore"]["save_state_date"] = self.current_date
        
        # Update prompts
        if "llmSystemPrompt" in config:
            new_core["agentCore"]["prompts"]["agentPrompts"]["llmSystemPrompt"] = config["llmSystemPrompt"]
        if "llmBoosterPrompt" in config:
            new_core["agentCore"]["prompts"]["agentPrompts"]["llmBoosterPrompt"] = config["llmBoosterPrompt"]
        if "visionSystemPrompt" in config:
            new_core["agentCore"]["prompts"]["agentPrompts"]["visionSystemPrompt"] = config["visionSystemPrompt"]
        if "visionBoosterPrompt" in config:
            new_core["agentCore"]["prompts"]["agentPrompts"]["visionBoosterPrompt"] = config["visionBoosterPrompt"]
            
        # Update command flags
        if "commandFlags" in config:
            new_core["agentCore"]["commandFlags"].update(config["commandFlags"])
            
        return new_core

    def storeAgentCore(self, agent_id: str, core_config: Dict[str, Any]) -> None:
        """Store an agent configuration in the matrix."""
        core_json = json.dumps(core_config)
        self.agent_library.upsert(
            documents=[core_json],
            ids=[agent_id],  # No need for extra agent_ prefix, keep IDs clean
            metadatas=[{"agent_id": agent_id, "save_date": self.current_date}]
        )

    def loadAgentCore(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load an agent configuration from the library."""
        results = self.agent_library.get(ids=[agent_id])
        if results and results["documents"]:
            loaded_config = json.loads(results["documents"][0])
            self.agentCores = loaded_config
            return loaded_config
        return None

    def listAgentCores(self) -> list:
        """List all available agent cores."""
        all_agents = self.agent_library.get()
        agent_cores = []
        for metadata, document in zip(all_agents["metadatas"], all_agents["documents"]):
            agent_core = json.loads(document)  # Deserialize the JSON string into a dictionary
            agent_cores.append({
                "agent_id": metadata["agent_id"],
                "uid": agent_core["agentCore"].get("uid", "Unknown"),
                "version": agent_core["agentCore"].get("version", "Unknown"),
            })
        return agent_cores
    
    def _generateUID(self, core_config: Dict) -> str:
        """Generate a unique identifier (UID) based on the agent core configuration."""
        core_json = json.dumps(core_config, sort_keys=True)
        return hashlib.sha256(core_json.encode()).hexdigest()[:8]
    
    def mintAgent(self,
                  agent_id: str,
                  db_config: Optional[Dict] = None,
                  model_config: Optional[Dict] = None,
                  prompt_config: Optional[Dict] = None,
                  command_flags: Optional[Dict] = None) -> Dict:
        """Create a new agent with proper database initialization."""
        # Create agent-specific databases
        agent_db_paths = self.create_agent_databases(agent_id)
        
        # Merge with any custom db_config
        if db_config:
            agent_db_paths.update(db_config)
        
        # Create agent configuration
        new_config = self.getNewAgentCore()
        new_config["agentCore"]["agent_id"] = agent_id
        new_config["agentCore"]["save_state_date"] = self.current_date
        new_config["agentCore"]["version"] = 1
        new_config["agentCore"]["databases"] = agent_db_paths
        
        if model_config:
            new_config["agentCore"]["models"].update(model_config)
        if prompt_config:
            new_config["agentCore"]["prompts"].update(prompt_config)
        if command_flags:
            new_config["agentCore"]["commandFlags"].update(command_flags)
        
        new_config["agentCore"]["uid"] = self._generateUID(new_config)
        
        # Store the new agent
        self.storeAgentCore(agent_id, new_config)
        return new_config

    def resetAgentCore(self):
        """Reset the current agent core to base template state."""
        self.agentCores = self.getNewAgentCore()
        return self.agentCores

    def getCurrentCore(self) -> Dict:
        """Get the current agent core configuration."""
        return self.agentCores

    def updateCurrentCore(self, updates: Dict):
        """Update the current agent core with new values."""
        self._mergeConfig(self.agentCore["agentCore"], updates)
        self.agentCores["agentCore"]["version"] += 1
        self.agentCores["agentCore"]["uid"] = self._generateUID(self.agentCores)
        
    def _mergeConfig(self, base: Dict, updates: Dict):
        """Recursively merge configuration updates."""
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._mergeConfig(base[key], value)
            else:
                base[key] = value

    def deleteAgentCore(self, agent_id: str) -> None:
        """Remove an agent configuration from storage."""
        self.agent_library.delete(ids=[agent_id])

    def saveToFile(self, agent_id: str, file_path: str) -> None:
        """Save an agent configuration to a JSON file."""
        config = self.loadAgentCore(agent_id)
        if config:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)

    def loadAgentFromFile(self, file_path: str) -> None:
        """Load an agent configuration from a JSON file and store in matrix."""
        with open(file_path, 'r') as f:
            config = json.load(f)
            if "agentCore" in config and "agent_id" in config["agentCore"]:
                self.storeAgentCore(config["agentCore"]["agent_id"], config)
            else:
                raise ValueError("Invalid agent configuration file")
        
    def migrateAgentCores(self):
        """Add versioning and UID to existing agent cores."""
        print("Migrating agent cores to include versioning and UID...")
        all_agents = self.agent_library.get()
        for metadata, document in zip(all_agents["metadatas"], all_agents["documents"]):
            agent_core = json.loads(document)
            
            # Add versioning and UID if missing
            if "version" not in agent_core["agentCore"] or agent_core["agentCore"]["version"] is None:
                agent_core["agentCore"]["version"] = 1
            if "uid" not in agent_core["agentCore"] or agent_core["agentCore"]["uid"] is None:
                agent_core["agentCore"]["uid"] = self._generateUID(agent_core)
            
            # Save the updated agent core back to the database
            self.storeAgentCore(metadata["agent_id"], agent_core)
        print("Migration complete.")
 
    def createDatabase(self, db_name: str, db_path: str) -> None:
        """Create a new database for an agent."""
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS agent_data (id INTEGER PRIMARY KEY, data JSON)")
        print(f"Created database: {db_path}")

    def linkDatabase(self, agent_id: str, db_name: str, db_path: str) -> None:
        """Link a database to an existing agent."""
        agent = self.loadAgentCore(agent_id)
        if agent:
            agent["agentCore"]["databases"][db_name] = db_path
            self.storeAgentCore(agent_id, agent)
            print(f"Linked database '{db_name}' to agent '{agent_id}'")
        else:
            print(f"Agent '{agent_id}' not found")

    def importAgentCores(self, import_db_path: str) -> None:
        """
        Import agent cores from another agent_matrix.db file into the current system.
        
        Args:
            import_db_path (str): Path to the agent_matrix.db file to import from
            
        Raises:
            FileNotFoundError: If the import database file doesn't exist
            sqlite3.Error: If there's an error reading from or writing to the databases
        """
        if not os.path.exists(import_db_path):
            raise FileNotFoundError(f"Import database not found: {import_db_path}")
            
        print(f"Importing agent cores from: {import_db_path}")
        
        try:
            # Create a temporary agentMatrix instance for the import database
            import_matrix = agentMatrix(import_db_path)
            
            # Get all agents from the import database
            import_agents = import_matrix.get()
            
            if not import_agents["documents"]:
                print("No agents found in import database.")
                return
                
            # Store each imported agent in the current system
            for doc, id_, metadata in zip(import_agents["documents"], 
                                        import_agents["ids"], 
                                        import_agents["metadatas"]):
                try:
                    # Parse the agent configuration
                    agent_core = json.loads(doc)
                    
                    # Store the agent in the current system
                    self.storeAgentCore(id_, agent_core)
                    print(f"Imported agent: {id_}")
                    
                except json.JSONDecodeError:
                    print(f"Warning: Failed to parse agent configuration for {id_}")
                except Exception as e:
                    print(f"Warning: Failed to import agent {id_}: {str(e)}")
                    
            print(f"Import complete. {len(import_agents['documents'])} agents processed.")
            
        except Exception as e:
            raise Exception(f"Error importing agent cores: {str(e)}")
        
    def commandInterface(self):
        """Command-line interface for managing agents."""
        
        print("Enter commands to manage agent cores. Type '/help' for options.")
        
        while True:
            command = input("> ").strip()
            if command == "/help":
                print("Commands:")
                print("  /agentCores - List all agent cores.")
                print("  /showAgent <agent_id> - Show agents with the specified ID.")
                print("  /createAgent <template_id> <new_agent_id> - Mint a new agent.")
                print("  /createCustomAgent - Interactive custom agent creation.")
                print("  /createDatabase <name> <path> - Create a new database.")
                print("  /linkDatabase <agent_id> <name> <path> - Link database to agent.")
                print("  /storeAgent <file_path> - Store agentCore from json path.")
                print("  /exportAgent <agent_id> - Export agentCore to json.")
                print("  /deleteAgent <uid> - Delete an agent by UID.")
                print("  /resetAgent <uid> - Reset an agent to the base template.")
                print("  /chat <agent_id> - Start a chat session with an agent.")
                print("  /importAgents <db_path> - gets the agentCores from the given db path and stores them in the default agent_matrix.db")
                print("  /exit - Exit the interface.")
                
            elif command.startswith("/chat"):
                try:
                    _, agent_id = command.split()
                    self.chat_with_agent(agent_id)
                except ValueError:
                    print("Usage: /chat <agent_id>")
                except Exception as e:
                    print(f"⚠️ Error starting chat: {e}")
                    
            elif command == "/agentCores":
                agents = self.listAgentCores()
                for agent in agents:
                    print(f"ID: {agent['agent_id']}, UID: {agent['uid']}, Version: {agent['version']}")
                    
            elif command.startswith("/showAgent"):
                try:
                    _, agent_id = command.split()
                    agents = self.agent_library.get(ids=[agent_id])
                    if agents and agents["documents"]:
                        for document in agents["documents"]:
                            agent_core = json.loads(document)  # Deserialize the JSON document
                            print(json.dumps(agent_core, indent=4))  # Pretty-print the JSON structure
                    else:
                        print(f"No agents found with ID: {agent_id}")
                except ValueError:
                    print("Usage: /showAgent <agent_id>")
                    
            elif command.startswith("/createAgent"):
                _, template_id, new_agent_id = command.split()
                self.mintAgent(template_id, new_agent_id)
                print(f"Agent '{new_agent_id}' created successfully.")
                
            elif command.startswith("/storeAgent"):
                try:
                    # Debug print to see the full command
                    print(f"Received command: {command}")

                    _, file_path = command.split()

                    # Debug print to check the file path
                    print(f"File path: {file_path}")

                    with open(file_path, "r") as file:
                        agent_core = json.load(file)

                    # Debug print to check the loaded JSON content
                    print(f"Loaded JSON: {agent_core}")

                    if "agentCore" not in agent_core:
                        print("Invalid JSON structure. The file must contain an 'agentCore' object.")
                        return

                    agent_id = agent_core["agentCore"].get("agent_id")
                    uid = agent_core["agentCore"].get("uid")

                    # Debug print to check agent_id and uid
                    print(f"agent_id: {agent_id}, uid: {uid}")

                    if not agent_id or not uid:
                        print("Invalid agent core. Both 'agent_id' and 'uid' are required.")
                        return

                    # Check if this agent already exists in the database
                    existing_agents = self.agent_library.get(ids=[agent_id])

                    # Debug print to check existing agents
                    print(f"Existing agents: {existing_agents}")

                    for document in existing_agents["documents"]:
                        existing_core = json.loads(document)
                        if existing_core["agentCore"]["uid"] == uid:
                            # Update the existing agent
                            self.storeAgentCore(agent_id, agent_core)
                            print(f"Agent core '{agent_id}' with UID '{uid}' updated successfully.")
                            return

                    # Otherwise, create a new agent core
                    self.storeAgentCore(agent_id, agent_core)
                    print(f"Agent core '{agent_id}' with UID '{uid}' added successfully.")

                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                except json.JSONDecodeError:
                    print("Error decoding JSON from the file. Please check the file content.")
                except ValueError:
                    print("Usage: /storeAgent <file_path>")
                except Exception as e:
                    print(f"⚠️ Error storing agent core: {e}")

            elif command.startswith("/exportAgent"):
                try:
                    _, agent_id = command.split()
                    agents = self.agent_library.get(ids=[agent_id])
                    if agents and agents["documents"]:
                        for document in agents["documents"]:
                            agent_core = json.loads(document)
                            # Define the file path
                            file_path = f"{agent_id}_core.json"
                            with open(file_path, "w") as file:
                                json.dump(agent_core, file, indent=4)
                            print(f"Agent core saved to {file_path}")
                    else:
                        print(f"No agents found with ID: {agent_id}")
                except ValueError:
                    print("Usage: /exportAgent <agent_id>")
                except Exception as e:
                    print(f"⚠️ Error saving agent core: {e}")
                    
            elif command.startswith("/deleteAgent"):
                _, uid = command.split()
                self.deleteAgentCore(uid)
                print(f"Agent with UID '{uid}' deleted.")
                
            elif command.startswith("/resetAgent"):
                _, uid = command.split()
                agent = self.loadAgentCore(uid)
                if agent:
                    self.resetAgentCore()
                    print(f"Agent with UID '{uid}' reset.")

            elif command == "/createCustomAgent":
                try:
                    print("\nInteractive Custom Agent Creation")
                    agent_id = input("Enter agent ID: ")
                    
                    # Basic configuration
                    model_config = {}
                    print("\nModel Configuration (press Enter to skip):")
                    llm = input("Large Language Model: ")
                    if llm: model_config["large_language_model"] = llm
                    vision = input("Vision Model: ")
                    if vision: model_config["language_and_vision_model"] = vision
                    
                    # Prompt configuration
                    prompt_config = {"agentPrompts": {}}
                    print("\nPrompt Configuration (press Enter to skip):")
                    system_prompt = input("System Prompt: ")
                    if system_prompt: 
                        prompt_config["agentPrompts"]["llmSystemPrompt"] = system_prompt
                    
                    # Database configuration
                    db_config = {}
                    print("\nDatabase Configuration:")
                    while True:
                        db_name = input("\nEnter database name (or Enter to finish): ")
                        if not db_name: break
                        db_path = input(f"Enter path for {db_name}: ")
                        db_config[db_name] = db_path
                        create_db = input("Create this database? (y/n): ")
                        if create_db.lower() == 'y':
                            self.createDatabase(db_name, db_path)
                    
                    # Create the agent
                    agent = self.mintAgent(
                        agent_id=agent_id,
                        model_config=model_config,
                        prompt_config=prompt_config,
                        db_config=db_config
                    )
                    print(f"\nCreated custom agent: {agent_id}")
                    
                except Exception as e:
                    print(f"Error creating custom agent: {e}")
                    
            elif command.startswith("/createDatabase"):
                try:
                    _, db_name, db_path = command.split()
                    self.createDatabase(db_name, db_path)
                except ValueError:
                    print("Usage: /createDatabase  ")
            
            elif command.startswith("/linkDatabase"):
                try:
                    _, agent_id, db_name, db_path = command.split()
                    self.linkDatabase(agent_id, db_name, db_path)
                except ValueError:
                    print("Usage: /linkDatabase   ")

            elif command.startswith("/importAgents"):
                    try:
                        _, import_path = command.split()
                        self.importAgentCores(import_path)
                    except ValueError:
                        print("Usage: /importAgents <path_to_agent_matrix.db>")
                    except Exception as e:
                        print(f"⚠️ Error importing agents: {e}")
            
            elif command == "/exit":
                break
            
            else:
                print("Invalid command. Type '/help' for options.")

    def chat_with_agent(self, agent_id: str):
        """Interactive chat session with a specified agent."""
        #TODO add agentCores default conversation history db
        #TODO allow get access to default knowledge bases
        try:
            # Load the agent
            agent = self.loadAgentCore(agent_id)
            if not agent:
                print(f"Agent '{agent_id}' not found.")
                return

            # Check if Ollama is available
            try:
                import ollama
                OLLAMA_AVAILABLE = True
            except ImportError:
                print("Ollama package not installed. Please install with: pip install ollama")
                return

            print(f"\nStarting chat with {agent_id}...")
            print("Type 'exit' to end the conversation.\n")

            # Get the agent's configuration
            llm = agent["agentCore"]["models"]["large_language_model"]
            if not llm:
                print("No language model configured for this agent.")
                return

            # Construct system prompt
            system_prompt = (
                f"{agent['agentCore']['prompts']['user_input_prompt']} "
                f"{agent['agentCore']['prompts']['agentPrompts']['llmSystemPrompt']} "
                f"{agent['agentCore']['prompts']['agentPrompts']['llmBoosterPrompt']}"
            )

            while True:
                # Get user input
                user_input = input("\nYou: ").strip()
                if user_input.lower() == 'exit':
                    print("\nEnding chat session...")
                    break

                # Stream the response
                print("\nAssistant: ", end='', flush=True)
                stream = ollama.chat(
                    model=llm,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_input}
                    ],
                    stream=True,
                )

                for chunk in stream:
                    print(chunk['message']['content'], end='', flush=True)
                print()  # New line after response

        except Exception as e:
            print(f"\n⚠️ Error in chat session: {e}")

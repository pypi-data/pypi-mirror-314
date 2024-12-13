from .agentCores import agentCores

def main():
    print("\n=== Welcome to agentCores Management Interface ===\n")
    
    # Initialize agentCore
    cores = agentCores()
    
    # Migrate existing agent cores
    cores.migrateAgentCores()
    
    print("agentCore system initialized. Enter '/help' for a list of commands.\n")
    
    # Start the command-line interface
    cores.commandInterface()

if __name__ == "__main__":
    main()
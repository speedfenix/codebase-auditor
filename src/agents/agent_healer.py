import os
import sys

# 🌐 WORKSPACE BOOTSTRAP: Dynamically calculate and inject project root path
# This allows 'src.agents' absolute imports to resolve perfectly regardless of invocation strategy
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.agents.agent_graph import app

if __name__ == "__main__":
    print("🚀 Booting localized autonomous multi-file self-healing cycle...")
    initial_state = {
        "context_chunks": [],
        "findings": [],
        "pending_files": [],
        "current_file": "",
        "execution_history": []
    }
    
    try:
        # pass as keyword to match parameter name "input" (avoids type error from callers expecting
        # HealerState | Command | None)
        app.invoke(initial_state)
    except Exception as e:
        print("\n" + "="*70)
        print("🛑 GRAPH EXECUTION TERMINATED: Runtime Error Encountered")
        print("="*70)
        
        err_msg = str(e)
        if "503" in err_msg or "UNAVAILABLE" in err_msg:
            print("🚨 Upstream infrastructure error: Google's Gemini API is currently over-capacity.")
            print("👉 Fix: Wait a few moments for the traffic spike to subside and re-run.")
        elif "FileNotFoundError" in err_msg or "No such file" in err_msg:
            print("🚨 Local target resource error: A file path operation failed.")
            print(f"👉 Details: {err_msg}")
        elif "Connection refused" in err_msg or "6333" in err_msg:
            print("🚨 Database connection error: Unable to talk to the local Qdrant container instance.")
            print("👉 Fix: Ensure your database daemon is active (`docker start qdrant`).")
        else:
            print("🚨 An unexpected failure occurred inside the state orchestration nodes.")
            print(f"👉 Error Message: {err_msg}")
            
        print("-"*70)
        print("💡 Traceback noise suppressed. Run with debugging flags enabled if deep analysis is required.")
        print("="*70 + "\n")
        sys.exit(1)
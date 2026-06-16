from src.agents.state import HealerState

def select_next_target_node(state: HealerState) -> dict:
    queue = state.get("pending_files", [])
    if not queue:
        return {"current_file": ""}
    
    next_target = queue[0]
    remaining_queue = queue[1:]
    
    print(f"\n🔄 [QUEUE CONTROLLER] {len(queue)} items left. Popping '{next_target}' into active memory.")
    return {"current_file": next_target, "pending_files": remaining_queue}
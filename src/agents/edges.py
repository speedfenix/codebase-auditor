from src.agents.state import HealerState

def route_after_queue_check(state: HealerState) -> str:
    if not state.get("current_file"):
        print("\n🎉 All critical files successfully processed. Halting graph loop runtime.")
        return "complete"
    return "continue"
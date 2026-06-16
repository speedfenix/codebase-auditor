from langgraph.graph import StateGraph, END
from .state import HealerState
from .edges import route_after_queue_check
from .nodes import (
    fetch_context_node,
    analyze_and_route_node,
    select_next_target_node,
    auto_heal_node,
)

workflow = StateGraph(HealerState)

# Append Independent Nodes
workflow.add_node("fetch_context", fetch_context_node)
workflow.add_node("analyze_route", analyze_and_route_node)
workflow.add_node("select_next_target", select_next_target_node)
workflow.add_node("auto_heal_node", auto_heal_node)

# Map Fixed Execution Edges
workflow.set_entry_point("fetch_context")
workflow.add_edge("fetch_context", "analyze_route")
workflow.add_edge("analyze_route", "select_next_target")

# Map Evaluation Router Loops
workflow.add_conditional_edges(
    "select_next_target",
    route_after_queue_check,
    {
        "continue": "auto_heal_node",
        "complete": END
    }
)
workflow.add_edge("auto_heal_node", "select_next_target")

app = workflow.compile()
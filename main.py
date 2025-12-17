from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState
from My_agents import supervisor, researcher, writer, check_answer


def build_graph():
    memory = MemorySaver()
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor)
    graph.add_node("research", researcher)
    graph.add_node("write", writer)
    graph.add_node("check", check_answer)

    graph.set_entry_point("supervisor")

    # ONE-WAY FLOW
    graph.add_edge("supervisor", "research")
    graph.add_edge("research", "write")
    graph.add_edge("write", "check")

    graph.add_conditional_edges(
        "check",
        lambda state: "end" if state["satisfied"] else "end",
        {
            "end": END,
        },
    )

    return graph.compile(checkpointer=memory)


if __name__ == "__main__":
    app = build_graph()

    print("Chat with the agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # NEW question per chat turn
        state = {
            "question": user_input,
            "research_notes": [],
            "answer": "",
            "satisfied": False,
            "user_feedback": "",
        }

        while True:
            state["satisfied"] = False

            result = app.invoke(
                state,
                config={"configurable": {"thread_id": "demo-thread"},
                "recursion_limit": 10 }
            )

            print("\nAgent:", result["answer"])

            feedback = input("\nAre you satisfied? (yes / no): ")
            state["user_feedback"] = feedback

            if feedback.lower() in ["yes", "y", "satisfied"]:
                break

        print()  # spacing between chats

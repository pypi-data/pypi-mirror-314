import os

from typing import TypedDict
from langgraph.graph import StateGraph

from researchgraph.nodes.writingnode.text2script_node import Text2ScriptNode


class State(TypedDict):
    code_string: str
    script_save_path: str


SAVE_DIR = os.environ.get("SAVE_DIR", "/workspaces/researchgraph/data")


def test_ext2script_node():
    filename = "test.py"
    graph_builder = StateGraph(State)
    graph_builder.add_node(
        "text2script",
        Text2ScriptNode(
            input_key=["code_string"],
            output_key=["script_save_path"],
            save_file_path=os.path.join(SAVE_DIR, filename),
        ),
    )
    graph_builder.set_entry_point("text2script")
    graph_builder.set_finish_point("text2script")
    graph = graph_builder.compile()

    state = {
        "code_string": "import test",
    }

    assert graph.invoke(state, debug=True)

import structlog
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.agents.graphutils import is_internal_node, is_skip_kind

# from mtmai.agents.task_graph.task_graph import TaskGraph
from mtmai.core.coreutils import is_in_dev
from mtmai.workflows.ctx import init_step_context
from mtmai.workflows.step_base import MtFlowBase
from mtmai.workflows.wfapp import wfapp

LOG = structlog.get_logger()
HUMEN_INPUT_NODE = "human_input"


class BlogAutoParams(BaseModel):
    threadId: str | None = None
    blogId: str


class BlogAutoResults(BaseModel):
    blogId: str


@wfapp.workflow(on_events=["blog:auto"])
class GraphFlow:
    @wfapp.step(timeout="10m", retries=3)
    async def call_agent(self, hatctx: Context):
        init_step_context(hatctx)
        return await StepGraph(hatctx).run()


class StepGraph(MtFlowBase):
    def __init__(self, ctx: Context):
        self.ctx = ctx

    # async def run(self):
    #     input = BlogAutoParams.model_validate(self.ctx.workflow_input())
    #     # self.emit("hello graph")
    #     thread = RunnableConfig(threadId=input.threadId)

    #     blog_graph = await TaskGraph().build_graph()

    #     checkpointer = MemorySaver()
    #     # db_checkpointer = await mtmai_context.get_graph_checkpointer()
    #     graph = (await self.build_graph()).compile(
    #         checkpointer=checkpointer,
    #         # interrupt_after=["human"],
    #         interrupt_before=[
    #             HUMEN_INPUT_NODE,
    #         ],
    #         debug=True,
    #     )

    #     if is_in_dev():
    #         image_data = graph.get_graph(xray=1).draw_mermaid_png()
    #         save_to = "./.vol/taskrunner_graph.png"
    #         with open(save_to, "wb") as f:
    #             f.write(image_data)
    #     # return graph

    #     await self.run_graph(thread, blog_graph, input)
    #     return BlogAutoResults(blogId=input.blogId)

    async def run_graph(
        self, thread: RunnableConfig, graph: CompiledGraph, inputs=None, messages=None
    ):
        async for event in graph.astream_events(
            inputs,
            version="v2",
            config=thread,
            subgraphs=True,
        ):
            kind = event["event"]
            node_name = event["name"]
            data = event["data"]

            if not is_internal_node(node_name):
                if not is_skip_kind(kind):
                    LOG.info("[event] %s@%s", kind, node_name)
                    # mtmai_context.emit("logs", {"on": kind, "node_name": node_name})

            if kind == "on_chat_model_stream":
                yield data

            if kind == "on_chain_start":
                LOG.info("on_chain_start %s:", node_name)
                output = data.get("output")
                if node_name == "__start__":
                    pass

            if kind == "on_chain_end":
                LOG.info("on_chain_end %s:", node_name)
                output = data.get("output")
                if node_name == "__start__":
                    pass
                if node_name in [HUMEN_INPUT_NODE, "articleGen", "entry"]:
                    human_ouput_message = output.get("human_ouput_message")
                    LOG.info("human_ouput_message %s", human_ouput_message)
            if node_name == "on_chat_start_node":
                thread_ui_state = output.get("thread_ui_state")
                # if thread_ui_state:
                #     await context.emitter.emit(
                #         "ui_state_upate",
                #         jsonable_encoder(thread_ui_state),
                #     )

            if kind == "on_tool_start":
                # await context.emitter.emit(
                #     "logs",
                #     {
                #         "on": kind,
                #         "node_name": node_name,
                #     },
                # )
                pass

            if kind == "on_tool_end":
                output = data.get("output")
                # await context.emitter.emit(
                #     "logs",
                #     {
                #         "on": kind,
                #         "node_name": node_name,
                #         "output": jsonable_encoder(output),
                #     },
                # )
                pass

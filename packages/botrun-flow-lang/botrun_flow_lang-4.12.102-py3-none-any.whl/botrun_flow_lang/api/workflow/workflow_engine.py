import asyncio
from copy import deepcopy
import time
from typing import List, Dict, Any, AsyncGenerator
from botrun_flow_lang.models.nodes.base_node import BaseNode, NodeType
from botrun_flow_lang.models.workflow import Workflow, WorkflowItem
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunStartedEvent,
    NodeRunCompletedEvent,
    NodeRunStreamEvent,
    WorkflowRunStartedEvent,
    WorkflowRunCompletedEvent,
    WorkflowRunFailedEvent,
)


class WorkflowEngine:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.variable_pool: Dict[str, Dict[str, Any]] = {}
        self.execution_times = []

    async def execute(
        self, initial_inputs: Dict[str, Any]
    ) -> AsyncGenerator[NodeEvent, None]:
        yield WorkflowRunStartedEvent()
        self.variable_pool.update(initial_inputs)

        try:
            async for event in self._execute_items(self.workflow.items):
                yield event

            yield WorkflowRunCompletedEvent(
                outputs=self.variable_pool, execution_times=self.execution_times
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            yield WorkflowRunFailedEvent(error=str(e))

    async def _execute_items(
        self, items: List[WorkflowItem], variable_pool: Dict[str, Dict[str, Any]] = None
    ) -> AsyncGenerator[NodeEvent, None]:
        var_pool = variable_pool if variable_pool is not None else self.variable_pool

        for item in items:
            if item.node:
                time_start = time.time()
                yield NodeRunStartedEvent(
                    node_id=item.node.data.id,
                    node_title=item.node.data.title,
                    node_type=item.node.data.type.value,
                    is_print=item.node.data.print_start,
                )

                if item.node.data.type == NodeType.ITERATION:
                    async for event in self._execute_iteration(item.node, item.items):
                        yield event
                else:
                    async for event in item.node.run(var_pool):
                        if isinstance(event, NodeRunStreamEvent):
                            yield event
                        elif isinstance(event, NodeRunCompletedEvent):
                            item.node.update_variable_pool(var_pool, event.outputs)
                            time_end = time.time()
                            self.execution_times.append(
                                f"=======>Node {item.node.data.title} completed in {time_end - time_start} seconds"
                            )
                            yield event
                        else:
                            yield event

    async def _execute_iteration(
        self, iteration_node: BaseNode, sub_items: List[WorkflowItem]
    ) -> AsyncGenerator[NodeEvent, None]:
        input_list = iteration_node.get_variable(
            self.variable_pool,
            iteration_node.data.input_selector.node_id,
            iteration_node.data.input_selector.variable_name,
        )

        if not isinstance(input_list, list):
            raise ValueError(
                f"Input for IterationNode must be a list, got {type(input_list)}"
            )

        outputs = []
        is_async = iteration_node.data.is_async

        if is_async:
            tasks = []
            for index, item in enumerate(input_list):
                task_variable_pool = {}
                for key, value in self.variable_pool.items():
                    if isinstance(value, dict):
                        task_variable_pool[key] = value.copy()
                    else:
                        task_variable_pool[key] = value

                task_variable_pool[iteration_node.data.id] = {
                    "item": item,
                    "index": index,
                }

                async def create_task(var_pool, current_index, current_item):
                    events = []
                    sub_engine = WorkflowEngine(self.workflow)
                    sub_engine.variable_pool = var_pool

                    async for event in sub_engine._execute_items(sub_items):
                        events.append(event)
                        yield event

                    if iteration_node.data.output_selector.node_id:
                        output = iteration_node.get_variable(
                            var_pool,
                            iteration_node.data.output_selector.node_id,
                            iteration_node.data.output_selector.variable_name,
                        )
                        outputs.append(output)

                    yield NodeRunStreamEvent(
                        node_id=iteration_node.data.id,
                        node_title=iteration_node.data.title,
                        node_type=iteration_node.data.type.value,
                        chunk=f"Iteration {current_index + 1}/{len(input_list)} completed",
                        is_print=iteration_node.data.print_stream,
                    )

                tasks.append(
                    self._process_item_wrapper(
                        create_task(task_variable_pool, index, item)
                    )
                )

            completed_tasks = await asyncio.gather(*tasks)
            for events in completed_tasks:
                for event in events:
                    yield event
        else:
            for index, item in enumerate(input_list):
                self.variable_pool[iteration_node.data.id] = {
                    "item": item,
                    "index": index,
                }
                async for event in self._execute_items(sub_items):
                    yield event

                if iteration_node.data.output_selector.node_id:
                    output = iteration_node.get_variable(
                        self.variable_pool,
                        iteration_node.data.output_selector.node_id,
                        iteration_node.data.output_selector.variable_name,
                    )
                    outputs.append(output)

        if outputs:
            iteration_node.update_variable_pool(self.variable_pool, {"output": outputs})
            yield NodeRunCompletedEvent(
                node_id=iteration_node.data.id,
                node_title=iteration_node.data.title,
                node_type=iteration_node.data.type.value,
                outputs={"output": outputs},
                complete_output=iteration_node.data.complete_output,
                is_print=iteration_node.data.print_complete,
            )

    async def _process_item_wrapper(self, generator):
        events = []
        async for event in generator:
            events.append(event)
        return events


async def run_workflow(
    workflow: Workflow, initial_inputs: Dict[str, Any]
) -> AsyncGenerator[NodeEvent, None]:
    engine = WorkflowEngine(workflow)
    async for event in engine.execute(initial_inputs):
        yield event

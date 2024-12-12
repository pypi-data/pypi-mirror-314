""" Shared pipeline configuration utility. """
import uuid
from typing import List, Optional, Dict, Union, Callable
from enum import Enum
from contextlib import contextmanager
from functools import wraps
import copy

from ipulse_shared_base_ftredge import (DataActionType, DataSourceType, DatasetScope, ProgressStatus)

COMPLETED_STATUSES = {
    ProgressStatus.COMPLETED,
    ProgressStatus.COMPLETED_WITH_WARNINGS,
    ProgressStatus.SKIPPED,
    ProgressStatus.CANCELLED
}

FAILED_STATUSES = {
    ProgressStatus.COMPLETED_WITH_ERRORS,
    ProgressStatus.FAILED,
    ProgressStatus.BLOCKED,
}

PENDING_STATUSES = {
    ProgressStatus.NOT_STARTED,
    ProgressStatus.IN_PROGRESS,
    ProgressStatus.PAUSED
}

class PipelineTask:
    """
    Represents a single task in a pipeline.
    """
    def __init__(
        self,
        n: str,
        a: Optional[DataActionType] = None,
        s: Optional[DataSourceType] = None,
        d: Optional[DataSourceType] = None,
        scope: Optional[DatasetScope] = None,
        dependencies: Optional[List[str]] = None,
        enabled: bool = True,
        config: Optional[Dict] = None,
    ):
        """
        Initialize a PipelineTask.
        :param n: Name of the task.
        :param s: Source of data for the task.
        :param a: Action to perform.
        :param d: Destination for the task output.
        :param scope: Scope of the dataset being processed.
        :param dependencies: List of task names that this task depends on.
        :param config: Task-specific configuration.
        :param enabled: Whether the task is enabled.
        """
        self.id=uuid.uuid4()
        self.name = n
        self.action = a
        self.source = s
        self.destination = d
        self.data_scope = scope
        self.dependencies = dependencies or []
        self.config = config or {}
        self.enabled = enabled
        self._status = ProgressStatus.NOT_STARTED
        # self.completed = False  # Tracks whether the step is completed
        self.pipeline_flow = None  # Reference to the parent PipelineFlow

    @property
    def is_completed(self) -> bool:
        """Check if task is completed based on status"""

        return self.status in COMPLETED_STATUSES
    
    @property
    def is_failed(self) -> bool:
        """Check if task is failed based on status"""

        return self.status in FAILED_STATUSES
    
    @property
    def is_finished(self) -> bool:
        """Check if task is finished based on status"""

        return self.status not in PENDING_STATUSES
    
    @property
    def is_pending(self) -> bool:
        """Check if task is pending based on status"""
        return self.status in PENDING_STATUSES
    
    @property
    def status (self) -> ProgressStatus:
        return self._status
    
    @status.setter
    def status(self, s:ProgressStatus):
        self._status = s
        

    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """
        Associate the task with a pipeline flow.
        :param pipeline_flow: The parent PipelineFlow.
        """
        self.pipeline_flow = pipeline_flow

    def validate(self, set_status:Optional[ProgressStatus]) -> bool:
        """
        Ensure the task is enabled and all dependencies are completed.
        :param pipeline_flow: The PipelineFlow instance managing tasks.
        :return: True if the task is ready to execute; otherwise, raise an exception.
        """
        if not self.enabled:
            self.status = ProgressStatus.SKIPPED
            return False
        if self.dependencies:
            for dependency in self.dependencies:
                dep_task = self.pipeline_flow.get_step(dependency)
                if not dep_task.is_completed:
                    self.status = ProgressStatus.NOT_STARTED
                    raise ValueError(f"Dependency '{dependency}' for task '{self.name}' is not completed.")
        self.status = set_status
        return True


    def __str__(self):
        status_symbol = "✔" if self.is_completed else "✖"
        parts = [f"[{status_symbol} {self.status.value}] {self.name}"]
        if self.action:
            parts.append(self.action.value)
        if self.source:
            parts.append(f"from {self.source.value}")
        if self.destination:
            parts.append(f"to {self.destination.value}")
        if self.data_scope:
            parts.append(f"scope={self.data_scope.value}")
        return f"{' :: '.join(parts)}"


class PipelineIterationTemplate:
    """
    Represents a single iteration of a dynamic iteration group.
    """
    def __init__(self,
                 steps: List[Union['PipelineTask', 'PipelineDynamicIterationGroup']]):
        # self.iteration_ref = iteration_ref
        self.steps: Dict[str, Union['PipelineTask', 'PipelineDynamicIterationGroup']] = {step.name: step for step in steps}

    def clone_steps(self) -> Dict[str, Union['PipelineTask', 'PipelineDynamicIterationGroup']]:
        """Create a deep copy of the steps for a new iteration."""
        
        return {name: copy.deepcopy(step) for name, step in self.steps.items()}
    
    @property
    def nb_tasks(self) -> int:
        return sum(
            step.nb_tasks() if hasattr(step, 'nb_tasks') else 1
            for step in self.steps.values() if step.enabled
        )
    
    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """Associate the iteration's tasks with the pipeline flow."""
        for step in self.steps.values():
            step.set_pipeline_flow(pipeline_flow)

    def __str__(self):
        # iteration_status = f"[Iteration {self.iteration_ref} :: Status: {self.status.value}]"
        steps_str = "\n".join(f"    {str(step)}" for step in self.steps.values())
        # return f"{iteration_status}\n{steps_str}"
        return steps_str
    

class PipelineIteration:
    """
    Represents a single iteration of a dynamic iteration group.
    """

    def __init__(self,
                 iteration_template: PipelineIterationTemplate,
                 iteration_ref: Union[int, str]):
        self.iteration_ref = iteration_ref
        self.steps = iteration_template.clone_steps()
        self._status = ProgressStatus.NOT_STARTED
        self.pipeline_flow = None  # Reference will be set later

    @property
    def status(self) -> ProgressStatus:
        return self._status
    
    @status.setter
    def status(self, s: ProgressStatus):
        self._status = s

    @property
    def is_completed(self) -> bool:
        return all(step.is_completed for step in self.steps.values())

    @property
    def is_failed(self) -> bool:
        return any(step.is_failed for step in self.steps.values())

    @property
    def is_finished(self) -> bool:
        return self.is_completed or self.is_failed

    @property
    def is_pending(self) -> bool:
        return not self.is_finished

    @property
    def nb_tasks(self) -> int:
        return sum(
            step.nb_tasks() if hasattr(step, 'nb_tasks') else 1
            for step in self.steps.values() if step.enabled
        )

    ######## TODO ENSURE THIS IS CALCULATED TAKING INTO ACCOUNT THE NUMBER OF TASKS IN THE ITERATION AND POSSIBLY DYNAMIC ITERATION GROUPS WITHIN
    @property
    def progress_percentage(self) -> float:
        """
        Compute the progress percentage for the iteration.
        :return: Progress as a float percentage.
        """
        pass



    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """Associate the iteration's tasks with the pipeline flow."""
        self.pipeline_flow = pipeline_flow
        for step in self.steps.values():
            step.set_pipeline_flow(pipeline_flow)

    def __str__(self):
        iteration_status = f"[Iteration {self.iteration_ref} :: Status: {self.status.value}]"
        steps_str = "\n".join(f"    {str(step)}" for step in self.steps.values())
        return f"{iteration_status}\n{steps_str}"
    

class PipelineDynamicIterationGroup:
    def __init__(self, 
                 name: str,
                 iteration_template: PipelineIterationTemplate,
                 enabled: bool = True,
                 dependencies: Optional[List[str]] = None,
                 max_iterations: Optional[int] = 100,
                 ):
        """
        Initialize the PipelineDynamicIterationGroup.

        :param name: Name of the loop group.
        :param task_templates: Templates of tasks that will be cloned for each iteration.
        :param enabled: Whether the loop group is enabled.
        :param dependencies: List of dependencies.
        :param max_iterations: Maximum number of iterations allowed. Useful to ensure termination within Cloud Function or other Execution environment.
        """
        self.name = name
        self.enabled = enabled
        self.dependencies = dependencies or []
        self.iteration_template:PipelineIterationTemplate = iteration_template
        # self.iterations: List[PipelineIteration] = []
        self.iteration_statuses: Dict[Union[int, str], ProgressStatus] = {}
        self._total_iterations = 0
        self._iterations: Dict[Union[int, str], PipelineIteration] = {}
        self.max_iterations = max_iterations
        self._status = ProgressStatus.NOT_STARTED  # New status enum
        self.pipeline_flow : PipelineFlow =None  # Reference will be set later

    
    
    @property
    def total_iterations(self) -> int:
        return self._total_iterations
    
    @total_iterations.setter
    def total_iterations(self, n: int):
        self._total_iterations = n

    @property
    def status(self) -> ProgressStatus:
        return self._status
        
    @status.setter
    def status(self, s:ProgressStatus):
        self._status = s
    
    @property
    def iterations(self) -> Dict[Union[int, str], PipelineIteration]:
        return self._iterations
    
    
    def set_iterations(self, iteration_refs: List[Union[int, str]]):
        self._iterations = {
            ref: PipelineIteration(self.iteration_template, ref)
            for ref in iteration_refs
        }
        for iteration in self.iterations.values():
            iteration.set_pipeline_flow(self.pipeline_flow)
        self.total_iterations = len(self.iterations)
        self.calculate_status()

    def get_iteration(self, iteration_ref: Union[int, str]) -> PipelineIteration:
        return self.iterations[iteration_ref]
    
    def add_iteration(self, iteration_ref: Union[int, str]):
        self.iterations[iteration_ref] = PipelineIteration(self.iteration_template, iteration_ref)
        self.total_iterations = len(self.iterations)
        self.calculate_status()
    
    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
            """Associate the loop group and its iterations with the pipeline flow."""
            self.pipeline_flow = pipeline_flow

    def add_iteration_status(self, iteration_ref: Union[int,str], status: ProgressStatus):
        """Add a status for a specific iteration."""
        self.iteration_statuses[iteration_ref] = status
        self.calculate_status_by_iter_statuses()

    
    def get_iteration_status(self, iteration_ref: Union[int,str]) -> ProgressStatus:
        """Retrieve the status for a specific iteration."""
        return self.iteration_statuses.get(iteration_ref, ProgressStatus.NOT_STARTED)
    
    def calculate_status(self):

        if self.total_iterations >0 :
            if all(iteration.is_completed for iteration in self.iterations.values()):
                self._status = ProgressStatus.COMPLETED
            elif all(iteration.is_pending for iteration in self.iterations.values()):
                self._status = ProgressStatus.NOT_STARTED
            elif any(iteration.is_failed for iteration in self.iterations.values()):
                self._status = ProgressStatus.FAILED
            else:
                self._status = ProgressStatus.IN_PROGRESS

    # def get_total_statuses_by_category(self) -> ProgressStatus:
    #     """Get the total number of iterations for each status category."""
    #     status_counts = {
    #         status: sum(1 for s in self.iteration_statuses.values() if s == status)
    #         for status in ProgressStatus
    #     }
    #     return status_counts
    
    def get_total_statuses_by_category(self) -> Dict[str, int]:
        """
        Returns a dictionary with counts of iterations in each status category: 'completed', 'failed', 'pending'.
        """
        statuses = {
            'completed': 0,
            'failed': 0,
            'pending': 0
        }
        for iteration in self.iterations.values():
            if iteration.is_completed:
                statuses['completed'] += 1
            elif iteration.is_failed:
                statuses['failed'] += 1
            else:
                statuses['pending'] += 1
        return statuses

    def calculate_status_by_iter_statuses(self):
        """Update the status of the loop group based on iterations."""
        if self.total_iterations > 0:
            if self.iteration_statuses:
                if len(self.iteration_statuses) == self.total_iterations:   
                    if all(status in COMPLETED_STATUSES for status in self.iteration_statuses.values()):
                        self._status = ProgressStatus.COMPLETED
                    elif all(status ==ProgressStatus.NOT_STARTED for status in self.iteration_statuses.values()):
                        self._status = ProgressStatus.NOT_STARTED
                    elif all (status in FAILED_STATUSES for status in self.iteration_statuses.values()):
                        self._status = ProgressStatus.FAILED
                    elif any(status in FAILED_STATUSES for status in self.iteration_statuses.values()):
                        self._status = ProgressStatus.COMPLETED_WITH_ERRORS
                    elif any(status in PENDING_STATUSES for status in self.iteration_statuses.values()):
                        self._status = ProgressStatus.IN_PROGRESS
                else :
                    self._status = ProgressStatus.IN_PROGRESS
            else:
                self._status = ProgressStatus.NOT_STARTED
        else:
            self._status=ProgressStatus.SKIPPED

    def get_step_statuses_across_iterations(self, step_name: str) -> Dict[str, int]:
        """
        Get aggregated status counts for a specific task across all iterations.
        """
        statuses = {
            'completed': 0,
            'failed': 0,
            'pending': 0
        }
        
        for iteration in self.iterations.values():
            if step_name in iteration.steps:
                step = iteration.steps[step_name]
                if step.is_completed:
                    statuses['completed'] += 1
                elif step.is_failed:
                    statuses['failed'] += 1
                else:
                    statuses['pending'] += 1
                    
        return statuses


    @property
    def is_completed(self) -> bool:
        """Check if all iterations are completed."""
        return self.calculate_status() in COMPLETED_STATUSES
    @property
    def is_failed(self) -> bool:
        """Check if any iteration has failed."""
        return self.calculate_status() in FAILED_STATUSES
    @property
    def is_finished(self) -> bool:
        """Check if all iterations are finished."""
        return self.calculate_status() not in PENDING_STATUSES
    @property
    def is_pending(self) -> bool:
        """Check if any iteration is pending."""
        return self.calculate_status() in PENDING_STATUSES


    def validate(self, set_status:Optional[ProgressStatus]=ProgressStatus.IN_PROGRESS) -> bool:
        """
        Ensure the Group is enabled and all dependencies are completed.
        """

        if not self.enabled or self.total_iterations == 0:
            self.status = ProgressStatus.SKIPPED
            return True # Return True as the group is skipped
        if self.max_iterations< self.total_iterations:
            self.status = ProgressStatus.CANCELLED
            raise ValueError(f"Total iterations {self.total_iterations} cannot be greater than max iterations {self.max_iterations}")
        if self.dependencies:
            for dependency in self.dependencies:
                dep_task = self.pipeline_flow.get_step(dependency)
                if not dep_task.is_completed:
                    self.status = ProgressStatus.BLOCKED
                    return False
        self.status = set_status
        
        return True


    @property
    def progress_percentage(self) -> float:
        if self.max_iterations == 0:
            return 0.0
        return (self.total_iterations / self.max_iterations) * 100

    def nb_tasks(self) -> int:
        """Get the total number of tasks in the group."""
        return self.iteration_template.nb_tasks * self.total_iterations

    def __str__(self):
        group_status = f"Group: {self.name} :: Status: {self.status.value}"
        iterations_str = str(self.iteration_template)
        return f"{group_status}\n{iterations_str}"




class PipelineFlow:
    """
    Enhanced Pipeline configuration utility with unique name enforcement.
    """

    def __init__(self, base_context_name:str):
        self.steps: Dict[str, Union['PipelineTask', 'PipelineDynamicIterationGroup']] = {}
        self.base_context=base_context_name

    def add_step(self, step: Union['PipelineTask', 'PipelineDynamicIterationGroup']):
        """
        Add a step which is a PipelineTask or PipelineLoopGroup to the pipeline.
        :param task_or_group: Single PipelineTask or PipelineLoopGroup.
        """
        if step.name in self.steps:
            raise ValueError(f"Step (Task, Group etc) with name '{step.name}' already exists in the pipeline.")
        self.steps[step.name] = step
        step.set_pipeline_flow(self)  # Associate the step with this pipeline flow

    def get_step(self, name: str, iteration_ref: Optional[Union[int, str]] = None) -> Union['PipelineTask', 'PipelineDynamicIterationGroup']:
        """
        Retrieve a task or group by name, searching recursively through all groups.
        :param name: Name of the task or group to retrieve.
        :return: Task or group with the given name.
        :raises KeyError: If no task or group exists with the given name.
        """
        # First, check top-level steps
        if name in self.steps:
            return self.steps[name]

        # Then, recursively check inside groups
        for step in self.steps.values():
            if isinstance(step, PipelineDynamicIterationGroup):
                if iteration_ref is not None:
                    if iteration_ref in step.iterations:
                        iteration = step.iterations[iteration_ref]
                        if name in iteration.steps:
                            return iteration.steps[name]
                else:
                    # No specific iteration requested - check iterations first
                    for iteration in step.iterations.values():
                        if name in iteration.steps:
                            return iteration.steps[name]
                    
                    # If not found in iterations, check template
                    if name in step.iteration_template.steps:
                        return step.iteration_template.steps[name]
                    

        raise KeyError(
            f"Task '{name}'" + 
            (f" in iteration {iteration_ref}" if iteration_ref else "") +
            " not found in pipeline"
        )
    
    
    def get_progress(self) -> dict:
        total_tasks = 0
        completed_tasks = 0
        failed_tasks = 0

        def traverse_tasks(task_collection):
            nonlocal total_tasks, completed_tasks, failed_tasks
            for task in task_collection.values():
                if isinstance(task, PipelineTask):
                    if task.enabled:
                        total_tasks += 1
                        if task.is_completed:
                            completed_tasks += 1
                        elif task.is_failed:
                            failed_tasks += 1
                elif isinstance(task, PipelineDynamicIterationGroup):
                    # Multiply by total iterations
                    total_tasks += task.nb_tasks()
                    # Assuming iteration statuses are updated
                    completed_tasks += sum(1 for status in task.iteration_statuses.values() if status in COMPLETED_STATUSES)
                    failed_tasks += sum(1 for status in task.iteration_statuses.values() if status in FAILED_STATUSES)
                    # Also consider tasks within iterations if needed

        traverse_tasks(self.steps)

        return {
            "total_tasks": total_tasks,
            "completed": completed_tasks,
            "failed": failed_tasks
        }
    
    def get_dependent_tasks(
    self,
    task: PipelineTask,
    iteration_ref: Optional[Union[int, str]] = None
    ) -> List[PipelineTask]:
        """
        Get all dependencies for a task, optionally from a specific iteration.
        
        Args:
            task: Task to get dependencies for
            iteration_ref: Optional reference to specific iteration
        """
        return [
            self.get_step(name=dep, iteration_ref=iteration_ref)
            for dep in task.dependencies
        ]

    def validate_dependencies(
        self,
        task: PipelineTask,
        iteration_ref: Optional[Union[int, str]] = None
        ) -> bool:
            """
            Check if all dependencies for a task are completed.
            
            Args:
                task: Task to validate dependencies for
                iteration_ref: Optional reference to specific iteration
            """
            try:
                dependent_tasks = self.get_dependent_tasks(task, iteration_ref)
                return all(dep.is_completed for dep in dependent_tasks)
            except KeyError as e:
                # Handle missing dependency
                raise ValueError(f"Missing dependency for task {task.name}: {str(e)}") from e
        
    # def get_pipeline_flow(self) -> str:
    #     """
    #     Generate a string representation of the pipeline flow, including only enabled tasks.
    #     """

    #     def _generate_flow(step, indent=0):
    #         if isinstance(step, PipelineTask):
    #             if not step.enabled:
    #                 return ""
    #             return f"{' ' * indent}>> {str(step)} [Status: {step.status.value}]"
    #         elif isinstance(step, PipelineDynamicIterationGroup):
    #             if not step.enabled:
    #                 return ""
    #             header = f"{' ' * indent}** [Status: {step.status.value}] {step.name}"
    #             # Display the flow of the iteration_template
    #             iteration_template_flow = "\n".join(
    #                 _generate_flow(sub_step, indent + 2)
    #                 for sub_step in step.iteration_template.steps.values()
    #                 if sub_step.enabled
    #             )
    #             return f"{header}\n{iteration_template_flow}" if iteration_template_flow.strip() else ""

    #     return "\n".join(
    #         _generate_flow(step) for step in self.steps.values() if step.enabled
    #     ).strip() + "\n"
    def get_pipeline_flow(self) -> str:
        """
        Generate a string representation of the pipeline flow, including task statistics across iterations.
        """
        def _generate_flow(step, indent=0):
            if isinstance(step, PipelineTask):
                if not step.enabled:
                    return ""
                return f"{' ' * indent}>> {step.name} [Status: {step.status.value}]"
            elif isinstance(step, PipelineDynamicIterationGroup):
                if not step.enabled:
                    return ""
                # Group header with iteration counts
                header = f"{' ' * indent}** {step.name}"
                if step.iterations:
                    iter_statuses = step.get_total_statuses_by_category()
                    iteration_info = (f"Total Iterations: {len(step.iterations)}, "
                                    f"Completed: {iter_statuses['completed']}, "
                                    f"Failed: {iter_statuses['failed']}, "
                                    f"Pending: {iter_statuses['pending']}")
                    header += f" [{iteration_info}]"
                else:
                    header += " [No iterations yet]"

                # Template tasks with their aggregated statuses
                template_flow = []
                for task_name in step.iteration_template.steps:
                    if step.iterations:
                        task_statuses = step.get_step_statuses_across_iterations(task_name)
                        task_info = (f"[Total: {sum(task_statuses.values())}, "
                                f"Completed: {task_statuses['completed']}, "
                                f"Failed: {task_statuses['failed']}, "
                                f"Pending: {task_statuses['pending']}]")
                        template_flow.append(
                            f"{' ' * (indent + 2)}>> {task_name} {task_info}"
                        )
                    else:
                        template_flow.append(
                            f"{' ' * (indent + 2)}>> {task_name}"
                        )

                return f"{header}\n{chr(10).join(template_flow)}" if template_flow else header

        return "\n".join(
            _generate_flow(step) for step in self.steps.values() if step.enabled
        ).strip() + "\n"
    
    # def get_pipeline_flow(self) -> str:
    #     """
    #     Generate a string representation of the pipeline flow, including only enabled tasks.
    #     """

    #     def _generate_flow(step, indent=0):
    #         if isinstance(step, PipelineTask):
    #             if not step.enabled:
    #                 return ""
    #             return f"{' ' * indent}>> {step.name} [Status: {step.status.value}]"
    #         elif isinstance(step, PipelineDynamicIterationGroup):
    #             if not step.enabled:
    #                 return ""
    #             header = f"{' ' * indent}** {step.name}"
    #             # If iterations exist, display counts by status
    #             if step.iterations:
    #                 statuses = step.get_total_statuses_by_category()
    #                 iteration_info = (f"Total Iterations: {len(step.iterations)}, "
    #                                   f"Completed: {statuses['completed']}, "
    #                                   f"Failed: {statuses['failed']}, "
    #                                   f"Pending: {statuses['pending']}")
    #                 header += f" [{iteration_info}]"
    #             else:
    #                 header += " [No iterations yet]"
    #             # Display the flow of the iteration template
    #             template_flow = "\n".join(
    #                 _generate_flow(sub_step, indent + 2)
    #                 for sub_step in step.iteration_template.steps.values()
    #                 if sub_step.enabled
    #             )
    #             return f"{header}\n{template_flow}" if template_flow.strip() else header
    #         else:
    #             return ""

    #     return "\n".join(
    #         _generate_flow(step) for step in self.steps.values() if step.enabled
    #     ).strip() + "\n"
    
    # def get_pipeline_flow(self) -> str:
    #     """
    #     Generate a string representation of the pipeline flow, including only enabled tasks.
    #     :return: String representing the pipeline flow.
    #     """

    #     def _generate_flow(task_or_group, indent=0):
    #         if isinstance(task_or_group, PipelineTask):
    #             if not task_or_group.enabled:
    #                 return ""  # Skip disabled tasks
    #             return f"{' ' * indent}>> {str(task_or_group)} [status={task_or_group.status.value}]"
    #         elif isinstance(task_or_group, PipelineDynamicIterationGroup):
    #             if not task_or_group.enabled:
    #                 return ""  # Skip disabled groups
    #             iteration_status = (
    #                 f"Iterations Started: {task_or_group.iterations_started}, Completed: {task_or_group.iterations_finished}/{task_or_group.iterations_total_required}"
    #                 if task_or_group.iterations_total_required
    #                 else f"Current Iterations: {task_or_group.iterations_started}, Completed: {task_or_group.iterations_finished} (Total unknown)"
    #             )
    #             header = f"{' ' * indent}** {task_or_group.name} :: {iteration_status} :: [Status={'✔' if task_or_group.is_completed else '✖'}]"
    #             inner_flow = "\n".join(
    #                 _generate_flow(t, indent + 2) for t in task_or_group.tasks.values() if t.enabled
    #             )
    #             return f"{header}\n{inner_flow}" if inner_flow.strip() else ""

    #     return "\n".join(
    #         _generate_flow(step) for step in self.steps.values() if step.enabled
    #     ).strip() + "\n"

    def get_pipeline_description(self) -> str:
        """
        Generate the complete pipeline description with base context and pipeline flow.
        :return: String representing the pipeline description.
        """
        return f"{self.base_context}\nflow:\n{self.get_pipeline_flow()}"
    



# class PipelineDynamicIterationGroup:
#     """
#     Represents a group of tasks that execute iteratively, with unique name enforcement.
#     """

#     def __init__(self, 
#                 name: str,
#                 tasks: List[Union['PipelineTask', 'PipelineDynamicIterationGroup']],
#                 enabled: bool = True,
#                 dependencies: Optional[List[str]] = None,
#                 iteration_started: int = 0,
#                 iteration_ended: Optional[int] = None,):
#         """
#         Initialize the PipelineLoopGroup.
#         :param name: Name of the loop group.
#         :param tasks: List of PipelineTask or nested PipelineLoopGroup.
#         """
#         self.name = name
#         self.enabled=enabled
#         self.tasks: Dict[str, Union['PipelineTask', 'PipelineDynamicIterationGroup']] = {}
#         self.dependencies = dependencies or []
#         # self.completed = False  # Tracks whether the group is completed
#         self.status = ProgressStatus.NOT_STARTED
#         self.pipeline_flow = None  # Reference to the parent PipelineFlow
#         self.current_iteration = iteration_started
#         self.iterations_total_required = iteration_ended # Total number of iterations
#         self.iterations_started = iteration_started # Number of iterations started
#         self.iterations_finished = iteration_started # Number of iterations completed
#         self.iterations_failed = 0
#         for task in tasks:
#             if task.name in self.tasks:
#                 raise ValueError(f"Task or group with name '{task.name}' already exists in group '{self.name}'.")
#             self.tasks[task.name] = task

#     @property
#     def progress_percentage(self) -> float:
#         """
#         Compute the progress percentage for iterations.
#         :return: Progress as a float percentage.
#         """
#         if self.iterations_total_required is None or self.iterations_total_required == 0:
#             return 0.0
#         return (self.iterations_finished / self.iterations_total_required) * 100
    
#     @property
#     def is_completed(self) -> bool:
#         """Check if group is completed based on iterations and status"""
#         if self.iterations_total_required is not None:
#             return (self.iterations_finished >= self.iterations_total_required and
#                    self.status in COMPLETED_STATUSES)
#         return True
    
#     @property
#     def is_finished(self) -> bool:
#         """Check if group is completed based on iterations and status"""
#         if self.iterations_total_required is not None:
#             return (self.iterations_finished >= self.iterations_total_required and 
#                     self.status not in PENDING_STATUSES)
#         return True
    

#     ######## TODO MAKE THIS NB ITERATIONS * NB TASKS IN ITERATION
#     @property
#     def nb_tasks(self) -> int:
#         """Get the total number of tasks in the group."""
#         return sum(task.nb_tasks for task in self.tasks.values())

    
#     def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
#         """
#         Associate the loop group with a pipeline flow and propagate to all tasks.
#         :param pipeline_flow: The parent PipelineFlow.
#         """
#         self.pipeline_flow = pipeline_flow
#         for task in self.tasks.values():
#             if isinstance(task, PipelineTask):
#                 task.set_pipeline_flow(pipeline_flow)
#             elif isinstance(task, PipelineDynamicIterationGroup):
#                 task.set_pipeline_flow(pipeline_flow)

#     def get_task(self, name: str):
#         """
#         Retrieve a task or nested group by name.
#         :param name: Name of the task or group to retrieve.
#         :return: Task or group with the given name.
#         :raises KeyError: If no task or group exists with the given name.
#         """
#         if name not in self.tasks:
#             raise KeyError(f"Task or group with name '{name}' not found in {self.name}.")
#         return self.tasks[name]
    
    
#     def validate(self,set_status:Optional[ProgressStatus]=ProgressStatus.IN_PROGRESS) -> bool:
#         """
#         Ensure the task is enabled and all dependencies are completed.
#         :param pipeline_flow: The PipelineFlow instance managing tasks.
#         :return: True if the task is ready to execute; otherwise, raise an exception.
#         """
#         if not self.enabled:
#             self.status = ProgressStatus.SKIPPED
#             return False
#         for dependency in self.dependencies:
#             dep_task = self.pipeline_flow.get_step(dependency)
#             if not dep_task.is_completed:
#                 self.status = ProgressStatus.BLOCKED
#                 raise ValueError(f"Dependency '{dependency}' not completed")
            
#         self.status = set_status
        
#         return True
    
#     def set_total_iterations(self, iteration_total: int):
#         """
#         Dynamically set the number of iterations for the loop group.
#         :param iteration_total: The total number of expected iterations.
#         """
#         self.iterations_total_required = iteration_total

#     def start_iteration(self):
#         """
#         Start a new iteration. Increment the iterations started count.
#         """
#         if self.iterations_total_required is not None and self.iterations_started >= self.iterations_total_required:
#             raise ValueError("Cannot start new iteration - limit reached")
#         self.status = ProgressStatus.IN_PROGRESS
#         self.iterations_started += 1

#     def complete_iteration(self):
#         """
#         Complete the current iteration. Increment the iterations completed count.
#         Mark the loop group as completed if all iterations are finished.
#         """
#         if self.iterations_finished < self.iterations_started:
#             self.iterations_finished += 1

#         self.status = ProgressStatus.COMPLETED

#     def fail_iteration(self):
#         """
#         Fail the current iteration. Increment the iterations completed count.
#         Mark the loop group as failed if all iterations are finished.
#         """
#         if self.iterations_finished < self.iterations_started:
#             self.iterations_finished += 1

#         if self.iterations_total_required is not None and self.iterations_finished >= self.iterations_total_required:
#             self.status = ProgressStatus.FAILED

#     def calculate_iteration_status(self):
#         """
#         Calculate the status of the loop group based on the status of its tasks.
#         """
#         if any(task.status in FAILED_STATUSES for task in self.tasks.values()):
#             self.status = ProgressStatus.FAILED
#         elif all(task.status in COMPLETED_STATUSES for task in self.tasks.values()):
#             self.status = ProgressStatus.COMPLETED
#         else:
#             self.status = ProgressStatus.IN_PROGRESS

#     def calculate_group_status(self):
#         """
#         Calculate the status of the loop group based on the status of its iterations.
#         """
#         if self.iterations_total_required is not None:
#             if self.iterations_finished >= self.iterations_total_required:
#                 self.status = ProgressStatus.COMPLETED
#             elif self.iterations_failed > 0:
#                 self.status = ProgressStatus.COMPLETED_WITH_ERRORS
#             else:
#                 self.status = ProgressStatus.IN_PROGRESS
#         else:
#             if all(task.is_completed for task in self.tasks.values()):
#                 self.status = ProgressStatus.COMPLETED
#             elif any(task.status in FAILED_STATUSES for task in self.tasks.values()):
#                 self.status = ProgressStatus.FAILED
#             else:
#                 self.status = ProgressStatus.IN_PROGRESS
       
        


#     def __str__(self):
#         completed_tasks = sum(
#             1 for task in self.tasks.values()
#             if task.is_completed
#         )
#         total_tasks = len(self.tasks)
#         iteration_progress = (
#             f"Iterations Started: {self.iterations_started}, Completed: {self.iterations_finished}/{self.iterations_total_required}"
#             if self.iterations_total_required
#             else f"Current Iterations Started: {self.iterations_started}, Completed: {self.iterations_finished} (Total unknown)"
#         )
#         progress_percent = f"Progress: {self.progress_percentage:.2f}%" if self.iterations_total_required else ""
#         status_symbol = "✔" if self.is_completed else "✖"
#         header = (
#             f"[{self.name} :: {iteration_progress} :: {progress_percent} :: Completed Tasks: {completed_tasks}/{total_tasks} :: Status={status_symbol}]"
#         )
#         inner_flow = "\n".join(str(task) for task in self.tasks.values())
        
#         return f"{header}\n{inner_flow}"


# class PipelineIterationTemplate:
#     """
#     Represents a single iteration of a dynamic iteration group.
#     """
#     def __init__(self,
#                  steps: List[Union['PipelineTask', 'PipelineDynamicIterationGroup']],
#                  iteration_ref: Optional [Union[int,str]]=None):
#         # self.iteration_ref = iteration_ref
#         self.steps: Dict[str, Union['PipelineTask', 'PipelineDynamicIterationGroup']] = {step.name: step for step in steps}
#         self._status = ProgressStatus.NOT_STARTED  # Initialize the status
#         self.pipeline_flow = None  # Reference will be set later

    
#     @property
#     def status (self) -> ProgressStatus:
#         return self._status
    
#     @status.setter
#     def status(self, s:ProgressStatus):
#         self._status = s

#     @property
#     def is_completed(self) -> bool:
#         """Check if the iteration is completed (all tasks completed without errors)."""
#         return all(step.is_completed for step in self.steps.values())

#     @property
#     def is_failed(self) -> bool:
#         """Check if the iteration has failed (any task failed)."""
#         return any(step.status in FAILED_STATUSES for step in self.steps.values())

#     @property
#     def is_finished(self) -> bool:
#         """Check if the iteration is finished (either completed or failed)."""
#         return self.is_completed or self.is_failed
    
#     @property
#     def is_pending(self) -> bool:
#         """Check if the iteration is pending (any task is pending)."""
#         return any(step.status in PENDING_STATUSES for step in self.steps.values())
    
#     @property
#     def nb_tasks(self) -> int:
#         """Get the total number of tasks in the iteration."""
#         n=0
#         for step in self.steps.values():
#             if step.enabled:
#                 if isinstance(step, PipelineDynamicIterationGroup):
#                     n+=len(step.nb_tasks)
#                 else:
#                     n+=1
#         return n

#     ######## TODO ENSURE THIS IS CALCULATED TAKING INTO ACCOUNT THE NUMBER OF TASKS IN THE ITERATION AND POSSIBLY DYNAMIC ITERATION GROUPS WITHIN
#     @property
#     def progress_percentage(self) -> float:
#         """
#         Compute the progress percentage for the iteration.
#         :return: Progress as a float percentage.
#         """
#         pass


#     def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
#         """Associate the iteration's tasks with the pipeline flow."""
#         self.pipeline_flow = pipeline_flow
#         for step in self.steps.values():
#             step.set_pipeline_flow(pipeline_flow)

#     def __str__(self):
#         # iteration_status = f"[Iteration {self.iteration_ref} :: Status: {self.status.value}]"
#         steps_str = "\n".join(f"    {str(step)}" for step in self.steps.values())
#         # return f"{iteration_status}\n{steps_str}"
#         return steps_str
from typing import Any, Dict, Optional, Union
import logging
import inspect
import traceback
import json
from ipulse_shared_base_ftredge import (LogLevel,
                                        log_warning,
                                        ProgressStatus)
from .context_log import ContextLog
from pprint import pformat
from .pipelineflow import  PipelineTask, PipelineDynamicIterationGroup

class PipelineEarlyTerminationError(Exception):
    """
    Exception raised for controlled pipeline termination.
    
    Attributes:
        reason: Detailed explanation of termination
        task_name: Name of task that triggered termination
        status_code: Optional status code for different termination types
        log_level: LogLevel for this termination
    """
    def __init__(
        self,
        reason: str,
        task: PipelineTask,
        context:str = "unknown",
        already_logged: bool = False
    ):
        self.reason = reason
        self.task_name = task.name
        task.status=ProgressStatus.FAILED
        self.already_logged = already_logged
        self.context=context
        super().__init__(f"Exception in context {context}, task '{task.name}': {reason} . - Pipeline Early Termination")


class PipelineIterationTerminationError(Exception):
    """
    Exception raised for controlled pipeline iteration termination.
    
    Attributes:
        reason: Detailed explanation of termination
        task_name: Name of task that triggered termination
        status_code: Optional status code for different termination types
        log_level: LogLevel for this termination
    """
    def __init__(
        self,
        reason: str,
        task: PipelineTask,
        context:str = "unknown",
        already_logged: bool = False
    ):
        self.reason = reason
        self.task_name = task.name
        self.already_logged = already_logged
        task.status=ProgressStatus.FAILED
        super().__init__(f"Exception in context {context} , task '{task.name}': {reason} . - Pipeline Iteration Termination")


# def format_detailed_error(e: Exception, operation_name: str) -> str:
#     parts = [
#         f"EXCEPTION during '{operation_name}':",
#         f"Type: {type(e).__name__}",
#         f"Message: {str(e)}",
#         f"Caused_by: {e.__cause__ or ''}",
#         f"Stack Trace:",
#         ''.join(traceback.format_tb(e.__traceback__))
#     ]
#     return ' \n '.join(parts)

def format_multiline_message(msg: Union[str, dict, set, Any]) -> str:
    """
    Format multiline messages for better readability in logs.
    Handles dictionaries, sets, and other serializable types.
    """
    try:
        # Use json.dumps for structured types
        if isinstance(msg, (dict, set, list, tuple)):
            return json.dumps(msg if not isinstance(msg, set) else list(msg), indent=2, default=str)
        return str(msg)
    except (TypeError, ValueError):
        # Fallback to pprint for non-serializable objects
        return pformat(msg, indent=2, width=80)

def format_detailed_error(e: Exception, operation_name: str) -> dict:
    """
    Format detailed error message as a dictionary.
    """
    return {
        "EXCEPTION during": operation_name,
        "Type": type(e).__name__,
        "Message": str(e),
        "Caused_by": str(e.__cause__ or ""),
        "Stack Trace": traceback.format_tb(e.__traceback__)  # List of stack trace lines
    }

def log_pipeline_step_exception(
    e: Exception,
    log_level: LogLevel,
    context:Optional[str]="a Step",
    pipelinemon = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> None:
    """Centralized error handler for pipeline steps"""
    
    caller_frame = inspect.currentframe().f_back
    func_name = caller_frame.f_code.co_name if caller_frame else "unknown_step"
    
    error_details = format_detailed_error(e, func_name)
    formatted_error = format_multiline_message(error_details)
    log_warning(
        msg=f"EXCEPTION in {context}: {formatted_error}",
        logger=logger,
        print_out=print_out
    )
    if pipelinemon:
        pipelinemon.add_log(ContextLog(
            level=log_level,
            e=e,
            subject=context,
            description=formatted_error
        ))

    if raise_e:
        raise e from e


def handle_operation_exception(
    e: Exception,
    result: Dict[str, Any],
    log_level: LogLevel,
    pipelinemon = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> None:
    """Centralized error handler for GCP operations"""
    

    caller_frame = inspect.currentframe().f_back
    operation_name = caller_frame.f_code.co_name if caller_frame else "unknown_operation"
    
    result["status"]["execution_state"] += f">>EXCEPTION: {log_level} "
    result["status"]["overall_status"] = "FAILED"
    error_details = format_detailed_error(e, operation_name)
    result["status"]["issues"] += f'>> {json.dumps(error_details, indent=2, default=str)}'
    formatted_status = format_multiline_message(result['status']) # for pretty printing
    log_warning(
        msg=f"EXCEPTION in OPERATION: {formatted_status}",
        logger=logger,
        print_out=print_out
    )
    if pipelinemon:
        pipelinemon.add_log(ContextLog(
            level=log_level,
            e=e,
            description=formatted_status
        ))
    if raise_e:
        raise e from e
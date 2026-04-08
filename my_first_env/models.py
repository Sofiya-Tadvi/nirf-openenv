from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from openenv.core.env_server.types import Action, Observation

class TableSnippet(BaseModel):
    name: str = Field(..., description="Name of the database table")
    columns: List[str] = Field(..., description="List of headers in the table")
    rows: List[Dict[str, Any]] = Field(..., description="The actual data rows")

class NIRFObservation(Observation): # MUST inherit from Observation
    task_description: str = Field(..., description="The NIRF goal")
    available_table: List[str] = Field(..., description="Tables available")
    query_result: Optional[TableSnippet] = Field(default=None)
    error_msg: Optional[str] = Field(default=None)
    nirf_rules: str = Field(default="")
    explanation: Optional[str] = Field(default=None)

class NIRFAction(Action):
    thought: Optional[str] = None
    sql_query: Optional[str] = None
    final_ans: Optional[str] = None
    to_submit: bool = False

class StepResult(BaseModel):
    observation: NIRFObservation
    reward: float
    done: bool
    info: Dict[str, Any]

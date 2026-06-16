from typing import List, TypedDict
from pydantic import BaseModel, Field

class HealerState(TypedDict):
    context_chunks: List[str]
    findings: List[dict]          
    pending_files: List[str]      
    current_file: str             
    execution_history: List[str]  

class CodeFlaw(BaseModel):
    file_path: str = Field(description="The name or path of the source file analyzed.")
    severity: str = Field(description="CRITICAL, MEDIUM, or LOW based on impact.")
    explanation: str = Field(description="Clear breakdown of the security vulnerability.")

class SecurityAuditReport(BaseModel):
    findings: List[CodeFlaw]
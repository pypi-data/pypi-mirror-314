from pydantic import BaseModel, JsonValue


class InitEnvironmentRequest(BaseModel):
    name: str
    trajectory_id: str
    status: str


class FinalEnvironmentRequest(BaseModel):
    trajectory_id: str
    status: str


class StoreAgentStateRequest(BaseModel):
    agent_id: str
    trajectory_id: str
    step: str
    state: JsonValue
    trajectory_timestep: int


class StoreEnvironmentFrameRequest(BaseModel):
    agent_state_point_in_time: str
    current_agent_step: str
    trajectory_id: str
    state: JsonValue

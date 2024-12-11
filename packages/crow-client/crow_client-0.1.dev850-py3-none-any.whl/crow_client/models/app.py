import re
from enum import StrEnum
from typing import ClassVar, Self

from ldp.alg.callbacks import Callback
from pydantic import BaseModel, Field, field_validator, model_validator


class Stage(StrEnum):
    DEV = "https://dev.api.scicraft.ai"
    PROD = "https://api.scicraft.ai"
    LOCAL = "http://localhost:8080"
    LOCAL_DOCKER = "http://host.docker.internal:8080"

    @classmethod
    def from_string(cls, stage: str) -> "Stage":
        """Convert a case-insensitive string to Stage enum."""
        try:
            return cls[stage.upper()]
        except KeyError as e:
            raise ValueError(
                f"Invalid stage: {stage}. Must be one of: {', '.join(cls.__members__)}"
            ) from e


class Step(StrEnum):
    BEFORE_TRANSITION = Callback.before_transition.__name__
    AFTER_AGENT_INIT_STATE = Callback.after_agent_init_state.__name__
    AFTER_AGENT_GET_ASV = Callback.after_agent_get_asv.__name__
    AFTER_ENV_RESET = Callback.after_env_reset.__name__
    AFTER_ENV_STEP = Callback.after_env_step.__name__
    AFTER_TRANSITION = Callback.after_transition.__name__


class DockerContainerConfiguration(BaseModel):
    cpu: str = Field(description="CPU allotment for the container")
    memory: str = Field(description="Memory allotment for the container")

    MINIMUM_MEMORY: ClassVar[int] = 2
    MAXIMUM_MEMORY: ClassVar[int] = 32

    @field_validator("cpu")
    @classmethod
    # The python library only supports 1, 2, 4, 8 CPUs
    # https://cloud.google.com/run/docs/reference/rpc/google.cloud.run.v2#resourcerequirements
    def validate_cpu(cls, v: str) -> str:
        valid_cpus = {"1", "2", "4", "8"}
        if v not in valid_cpus:
            raise ValueError("CPU must be one of: 1, 2, 4, or 8")
        return v

    @field_validator("memory")
    @classmethod
    def validate_memory(cls, v: str) -> str:
        # https://regex101.com/r/4kWjKw/1
        match = re.match(r"^(\d+)Gi$", v)

        if not match:
            raise ValueError("Memory must be in Gi format (e.g., '2Gi')")

        value = int(match.group(1))

        # GCP Cloud Run has min 512Mi and max 32Gi (32768Mi)
        # https://cloud.google.com/run/docs/configuring/services/memory-limits
        # due to the above mentioned restriction in the python client, we must
        # stay between 2Gi and 32Gi
        if value < cls.MINIMUM_MEMORY:
            raise ValueError("Memory must be at least 2Gi")
        if value > cls.MAXIMUM_MEMORY:
            raise ValueError("Memory must not exceed 32Gi")

        return v

    @model_validator(mode="after")
    def validate_cpu_memory_ratio(self) -> Self:
        cpu = int(self.cpu)

        match = re.match(r"^(\d+)Gi$", self.memory)
        if match is None:
            raise ValueError("Memory must be in Gi format (e.g., '2Gi')")

        memory_gi = int(match.group(1))
        memory_mb = memory_gi * 1024

        min_cpu_requirements = {
            2048: 1,  # 2Gi requires 1 CPU
            4096: 2,  # 4Gi requires 2 CPU
            8192: 4,  # 8Gi requires 4 CPU
            24576: 8,  # 24Gi requires 8 CPU
        }

        for mem_threshold, cpu_required in min_cpu_requirements.items():
            if memory_mb <= mem_threshold:
                if cpu < cpu_required:
                    raise ValueError(
                        f"For {self.memory} of memory, minimum required CPU is {cpu_required} CPU. Got {cpu} CPU"
                    )
                break

        return self

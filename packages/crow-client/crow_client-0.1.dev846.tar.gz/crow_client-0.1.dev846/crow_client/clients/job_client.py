import logging
from typing import ClassVar
from uuid import UUID, uuid4

import httpx
from aviary.env import Frame
from pydantic import BaseModel
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_exponential

from crow_client.models.app import Stage
from crow_client.models.rest import (
    FinalEnvironmentRequest,
    InitEnvironmentRequest,
    StoreAgentStateRequest,
    StoreEnvironmentFrameRequest,
)

logger = logging.getLogger(__name__)


class CrowJobClient:
    REQUEST_TIMEOUT: ClassVar[float] = 30.0  # sec
    MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
    RETRY_MULTIPLIER: ClassVar[int] = 1
    MAX_RETRY_WAIT: ClassVar[int] = 10

    def __init__(
        self,
        environment: str,
        agent: str,
        auth_token: str,
        base_uri: Stage = Stage.LOCAL,
        trajectory_id: str | UUID | None = None,
    ):
        self.base_uri = base_uri.value
        self.agent = agent
        self.environment = environment
        self.oauth_jwt = auth_token
        self.current_timestep = 0
        self.trajectory_id = self._cast_trajectory_id(trajectory_id)
        self.current_step: str | None = None

    @staticmethod
    def _cast_trajectory_id(provided_trajectory_id: str | UUID | None) -> str:
        if provided_trajectory_id is None:
            return str(uuid4())
        if isinstance(provided_trajectory_id, str):
            return provided_trajectory_id
        if isinstance(provided_trajectory_id, UUID):
            return str(provided_trajectory_id)
        raise ValueError("Invalid trajectory ID provided")

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def initialize_environment(self) -> None:
        """Initialize an environment with retry mechanism for handling transient failures."""
        data = InitEnvironmentRequest(
            name=self.environment,
            trajectory_id=self.trajectory_id,
            status="in progress",
        )
        async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
            response = await client.post(
                url=f"{self.base_uri}/environment-instance",
                json=data.model_dump(mode="json"),
                headers={"Authorization": f"Bearer {self.oauth_jwt}"},
            )
            response.raise_for_status()
            logger.debug(f"Environment initialized successfully, {self.environment}")
            return response.json()

    async def finalize_environment(self, status: str) -> None:
        data = FinalEnvironmentRequest(trajectory_id=self.trajectory_id, status=status)
        async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
            response = await client.post(
                url=f"{self.base_uri}/environment-status",
                json=data.model_dump(mode="json"),
                headers={"Authorization": f"Bearer {self.oauth_jwt}"},
            )
            response.raise_for_status()
            logger.debug(f"Environment updated with status {status}")

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def store_agent_state(self, step: str, state: BaseModel | dict) -> None:
        """Store agent state with retry mechanism."""
        self.current_step = step

        state_data = (
            state.model_dump(mode="json") if isinstance(state, BaseModel) else state
        )

        if state_data and state_data.get("transition"):
            timestep = state_data.get("transition", {}).get("timestep")
            if timestep is not None:
                self.current_timestep = timestep

        data = StoreAgentStateRequest(
            agent_id=self.agent,
            trajectory_id=self.trajectory_id,
            step=self.current_step,
            state=state_data,
            trajectory_timestep=self.current_timestep,
        )

        try:
            async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
                response = await client.post(
                    url=f"{self.base_uri}/agent-state",
                    json=data.model_dump(mode="json"),
                    headers={"Authorization": f"Bearer {self.oauth_jwt}"},
                )
                response.raise_for_status()
                logger.debug(f"Agent state stored successfully for step {step}")
                return response.json()
        except Exception:
            logger.exception(f"Unexpected error storing state for step {step}")
            raise

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def store_environment_frame(self, state: Frame) -> None:
        """Store environment frame with retry mechanism."""
        state_identifier = None
        if self.current_step is not None:
            state_identifier = (
                f"{self.agent}-{self.current_step}-{self.current_timestep}"
            )

        data = StoreEnvironmentFrameRequest(
            agent_state_point_in_time=state_identifier,
            current_agent_step=self.current_step,
            trajectory_id=self.trajectory_id,
            state=state.model_dump(mode="json"),
        )

        try:
            async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
                response = await client.post(
                    url=f"{self.base_uri}/environment-frame",
                    json=data.model_dump(mode="json"),
                    headers={"Authorization": f"Bearer {self.oauth_jwt}"},
                )
                response.raise_for_status()
                logger.debug(
                    f"Environment Frame stored successfully for state {state_identifier}"
                )
                return response.json()
        except Exception:
            logger.exception(
                f"Unexpected error storing state for state {state_identifier}"
            )
            raise

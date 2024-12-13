from ..core._types._huggingface import HFModelType
from ..core.agents.agent import Agent
from ..logging.logger import AgentLogger

class HFAgent(Agent):
    def __init__(self,
                 model:HFModelType="huggingface:Qwen/Qwen2.5-72B-Instruct",
                 api_key="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",
                 logger=AgentLogger(level="CRITICAL"),
                 *args,
                 **kwargs):
        super().__init__(model=model, api_key=api_key, logger=logger, *args, **kwargs)


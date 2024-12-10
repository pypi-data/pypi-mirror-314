from therix.core.pipeline_component import PipelineComponent
from therix.entities.models import ConfigType


class Trace(PipelineComponent):
    def __init__(self, config):
        config["host"] = "https://cloud-api.therix.ai"
        
        super().__init__(ConfigType.TRACE_DETAILS, "LANGFUSE", config)

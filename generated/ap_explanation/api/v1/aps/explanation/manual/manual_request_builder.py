from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .annotations.annotations_request_builder import AnnotationsRequestBuilder
    from .computations.computations_request_builder import ComputationsRequestBuilder

class ManualRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/v1/aps/explanation/manual
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new ManualRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/v1/aps/explanation/manual", path_parameters)
    
    @property
    def annotations(self) -> AnnotationsRequestBuilder:
        """
        The annotations property
        """
        from .annotations.annotations_request_builder import AnnotationsRequestBuilder

        return AnnotationsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def computations(self) -> ComputationsRequestBuilder:
        """
        The computations property
        """
        from .computations.computations_request_builder import ComputationsRequestBuilder

        return ComputationsRequestBuilder(self.request_adapter, self.path_parameters)
    


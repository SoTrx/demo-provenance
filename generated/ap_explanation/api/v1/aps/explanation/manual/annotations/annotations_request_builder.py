from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from .......models.annotation_result import AnnotationResult
    from .......models.h_t_t_p_validation_error import HTTPValidationError
    from .......models.pg_json import PgJson
    from .......models.removal_result import RemovalResult
    from .item.with_semiring_name_item_request_builder import WithSemiring_nameItemRequestBuilder

class AnnotationsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/v1/aps/explanation/manual/annotations
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new AnnotationsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/v1/aps/explanation/manual/annotations", path_parameters)
    
    def by_semiring_name(self,semiring_name: str) -> WithSemiring_nameItemRequestBuilder:
        """
        Gets an item from the ApiSdk.api.v1.aps.explanation.manual.annotations.item collection
        param semiring_name: Unique identifier of the item
        Returns: WithSemiring_nameItemRequestBuilder
        """
        if semiring_name is None:
            raise TypeError("semiring_name cannot be null.")
        from .item.with_semiring_name_item_request_builder import WithSemiring_nameItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["semiring_name"] = semiring_name
        return WithSemiring_nameItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def delete(self,body: PgJson, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[list[RemovalResult]]:
        """
        Remove provenance annotations from AP tables.Part of the manual explanation lifecycle. Call this afterPOST /aps/explanation/manual/computations to clean up annotations.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[list[RemovalResult]]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_delete_request_information(
            body, request_configuration
        )
        from .......models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: dict[str, type[ParsableFactory]] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .......models.removal_result import RemovalResult

        return await self.request_adapter.send_collection_async(request_info, RemovalResult, error_mapping)
    
    async def post(self,body: PgJson, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[list[AnnotationResult]]:
        """
        Annotate AP tables with all available semirings.Part of the manual explanation lifecycle. After annotating, compute viaPOST /aps/explanation/manual/computations, then clean up viaDELETE /aps/explanation/manual/annotations.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[list[AnnotationResult]]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from .......models.h_t_t_p_validation_error import HTTPValidationError

        error_mapping: dict[str, type[ParsableFactory]] = {
            "422": HTTPValidationError,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .......models.annotation_result import AnnotationResult

        return await self.request_adapter.send_collection_async(request_info, AnnotationResult, error_mapping)
    
    def to_delete_request_information(self,body: PgJson, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Remove provenance annotations from AP tables.Part of the manual explanation lifecycle. Call this afterPOST /aps/explanation/manual/computations to clean up annotations.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.DELETE, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def to_post_request_information(self,body: PgJson, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Annotate AP tables with all available semirings.Part of the manual explanation lifecycle. After annotating, compute viaPOST /aps/explanation/manual/computations, then clean up viaDELETE /aps/explanation/manual/annotations.
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> AnnotationsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: AnnotationsRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return AnnotationsRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class AnnotationsRequestBuilderDeleteRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class AnnotationsRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    


from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .pg_json_edge import PgJsonEdge
    from .pg_json_node import PgJsonNode

@dataclass
class PgJson(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The edges property
    edges: Optional[list[PgJsonEdge]] = None
    # The nodes property
    nodes: Optional[list[PgJsonNode]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> PgJson:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: PgJson
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return PgJson()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .pg_json_edge import PgJsonEdge
        from .pg_json_node import PgJsonNode

        from .pg_json_edge import PgJsonEdge
        from .pg_json_node import PgJsonNode

        fields: dict[str, Callable[[Any], None]] = {
            "edges": lambda n : setattr(self, 'edges', n.get_collection_of_object_values(PgJsonEdge)),
            "nodes": lambda n : setattr(self, 'nodes', n.get_collection_of_object_values(PgJsonNode)),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_collection_of_object_values("edges", self.edges)
        writer.write_collection_of_object_values("nodes", self.nodes)
        writer.write_additional_data_value(self.additional_data)
    


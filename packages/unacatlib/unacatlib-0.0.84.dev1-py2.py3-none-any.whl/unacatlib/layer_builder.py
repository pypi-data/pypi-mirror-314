from typing import TYPE_CHECKING
from syncer import sync

from .layer import Layer
from .layer_series import LayerSeries
from .address_component import AddressComponent
if TYPE_CHECKING:
  from .catalog import Catalog

from unacatlib.unacast.maps.v1 import LayerSpec, Layer as v1_Layer, AddressComponentValueSpec, LayerKind
from unacatlib.unacast.operator.v1 import CreateLayerRequest, CreateLayerSeriesRequest, CreateLayerSeriesResponse
from unacatlib.unacast.unatype import AvailabilityKind

class LayerBuilder(object):

    def __init__(self, catalog: "Catalog", given_id: str):
        self._catalog = catalog
        self.map_operator_service = catalog._client.map_operator_service

        self._given_id = given_id
        self._address_components = []
        self._display_name = None
        self._description = None
        self._feature_display_name = None
        self._feature_description = None
        self._feature_kind_display_name = None
        self._version = None
        self._attribution = None
        self._availability = AvailabilityKind.ALL
        self._layer_kind = LayerKind.INDEXED


    def with_display_name(self, display_name: str):
      self._display_name = display_name
      return self

    def with_description(self, description: str):
      self._description = description
      return self

    def with_feature_display_name(self, display_name: str):
      self._feature_display_name = display_name
      return self

    def with_feature_kind_display_name(self, feature_kind_display_name: str):
        self._feature_kind_display_name = feature_kind_display_name
        return self

    def with_feature_description(self, description: str):
      self._feature_description = description
      return self

    def with_version(self, version: str):
      self._version = version
      return self

    def with_availability(self, availability: AvailabilityKind):
        self._availability = availability
        return self

    def with_layer_kind(self, layer_kind: LayerKind):
        self._layer_kind = layer_kind
        return self

    def with_attribution(self, attribution: str):
      self._attribution = attribution
      return self

    def with_address_component(self, ac: AddressComponent, allow_empty_values: bool = False):
      self._address_components.append(AddressComponentValueSpec(component=ac.component, allow_empty_values=allow_empty_values))
      return self

    def getLayerSpec(self) -> LayerSpec:
      return LayerSpec(
        catalog_id=self._catalog._catalog.id,
        address_components=self._address_components,
        feature_display_name=self._feature_display_name,
        feature_description=self._feature_description,
        feature_kind_display_name=self._feature_kind_display_name,
        version=self._version,
        attribution=self._attribution
      )

    def create(self, skip_create_address_component: bool = False) -> Layer:
      res: v1_Layer = sync(
            self.map_operator_service.create_layer(CreateLayerRequest(
              given_id=self._given_id,
              availability=self._availability,
              spec=self.getLayerSpec(),
              display_name=self._display_name,
              description=self._description,
              layer_kind=self._layer_kind,
              skip_address_component=skip_create_address_component
            ))
      )
      return Layer(self._catalog, res)
    
    def create_as_layer_series(self) -> LayerSeries:
      res: CreateLayerSeriesResponse = sync(
            self.map_operator_service.create_layer_series(CreateLayerSeriesRequest(
              given_id=self._given_id,
              catalog_id=self._catalog._catalog.id,
              display_name=self._display_name,
              description=self._description,
              spec=self.getLayerSpec()
            ))
      )
      return LayerSeries(self._catalog, res.layer_series)
    

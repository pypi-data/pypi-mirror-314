from syncer import sync
from typing import TYPE_CHECKING, Tuple

from .layer import Layer

if TYPE_CHECKING:
  from .catalog import Catalog

from unacatlib.unacast.maps.v1 import Layer as v1_Layer, MapLayerSeries as v1_LayerSeries, LayerSpec
from unacatlib.unacast.operator.v1 import PrepareLayerSeriesRevisionRequest, PrepareLayerSeriesRevisionResponse


class LayerSeries(object):

    def __init__(self, catalog: "Catalog", layer_series_value: v1_LayerSeries):
        self._catalog = catalog
        self._layer_series = layer_series_value
        self._map_operator_service = catalog._client.map_operator_service

    @property
    def id(self):
        return self._layer_series.id
    
    @property
    def name(self):
        return self._layer_series.display_name

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return self._layer_series.to_dict()

    def prepare_revision(self, layer_spec: LayerSpec) -> Tuple[str, Layer]:
      prep: PrepareLayerSeriesRevisionResponse = sync(
        self._map_operator_service.prepare_layer_series_revision(PrepareLayerSeriesRevisionRequest(
          layer_series_id=self._layer_series.id,
          layer_spec=layer_spec,
        ))
      )
      return prep.layer_series_revision, self._catalog.layer(prep.layer_id)

    def publish_version(self, revision_id: str):
      raise "Publishing should be done through the catalog"
    

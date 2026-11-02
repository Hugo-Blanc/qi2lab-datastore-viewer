try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'unknown'


from ._reader import napari_get_reader
from ._sample_data import make_sample_data
from ._widget import (
    ExampleQWidget,
    ImageThreshold,
    threshold_autogenerate_widget,
    threshold_magic_widget,
)

__all__ = (
    'ExampleQWidget',
    'ImageThreshold',
    'make_sample_data',
    'napari_get_reader',
    'threshold_autogenerate_widget',
    'threshold_magic_widget',
)

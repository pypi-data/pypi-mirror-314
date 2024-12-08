from keras_hub.src.api_export import keras_hub_export

# Unique source of truth for the version number.
__version__ = "0.19.0.dev202412080355"


@keras_hub_export("keras_hub.version")
def version():
    return __version__

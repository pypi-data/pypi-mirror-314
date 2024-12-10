# GeoPortal Plugin for OneCode

This plugin wraps OneCode input and output elements so that they work seamlessly with the GeoPortal.
Compatible with OneCode 1.0.0+ only.

## CLI

To produce `interface.json` as well as `i18n` files, run from the root OneCode project:

```bash
geoportal-extract
```

## API

**Inputs**
Use `geo_` prefix in front of all OneCode elements, e.g. `geo_slider` instead of `slider`, etc.

**Outputs**

```python
geo_file_output(
    path: str,              # Path to the output file
    type: str,              # GeoPortal type, e.g. CSV, BlockModel, etc.
    prefix: str = "",       # Optional prefix to left-strip file path
    group: bool = False,    # True for GeoPortal multi-files (e.g. ShpFile)
    release: bool = False,  # True to record file as a release for the sign-off process
    key: str = None,        # Specific key in case file is reference in another workflow
    **kwargs                # Any additional properties to attach to the GeoPortal file
)
```

## Examples

Checkout the examples folders.

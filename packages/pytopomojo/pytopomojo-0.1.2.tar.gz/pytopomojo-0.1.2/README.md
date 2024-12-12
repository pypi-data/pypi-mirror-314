# PyTopoMojo

This project is a Python API Client that can be used to interact with [TopoMojo](https://github.com/cmu-sei/TopoMojo).  It is a work in progress, so not all TopoMojo API endpoints are implemented yet. 

## Installation

```
pip install pytopomojo
```

## Usage Example

```python
from pytopomojo import Topomojo

topomojo = Topomojo("<topomojo_url>", "<topomojo_api_key>")
topomojo.get_workspaces()
```
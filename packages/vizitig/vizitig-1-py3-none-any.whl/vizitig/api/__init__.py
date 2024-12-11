from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from vizitig.api.main import app, export_path
from vizitig.api.path import site
from vizitig.info import graphs_path

"""
Vizitig API
===========

This module is based on FastApi to do most of the work. Code in this module should
be mostly:
- boilerplate code to call the appropriate vizitig function
- a bit of tmpfile manipulation

API Layout
----------

The api code is mostly in the main submodule.
The api must serves some files (like the website directory)
that are provided here. 
To add a completely novel api endpoint, do it here exactly like for the export
and site endpoint. 

Specificities
-------------

FastApi decorator are overloaded to add the Python function name in the openapi signature.
Thanks to that, the JS front API client use the same function name.
As a consequence, instead of defining a route using

app.get("/foo/bar")

use the customly defined in the main submodule

vizitig.main.get("/foo/bar")

Be aware that the JS code might not handle so well optional argument or complexe interaction.


Long running process
--------------------

For long running vizitig function, wrap the function using async_subproc.
Otherwise, the API endpoint might be too busy to serve queries while doing
heavy tasks. Ex:

```python
from vizitig.api.async_utils import async_subproc
async_subproc(generate_graph)(tmp_path, graph_path_name(name))
````

Error Handling
--------------

Errors raise by Vizitig (VizitigException) are catched and lift to the front.
Errors raise by anything else will not be catched and raise a 500 server Error.
To avoid this, try/except those error and raise instead the appropriate HTTPException

In principle, Error 500 should never happens. If it happens, it means that some part of
the API is not handling an error appropriately. Please report the issue on the project
gitlab if it is the case.

"""


main_api = FastAPI()
main_api.mount("/api", app)
main_api.mount("/files", StaticFiles(directory=graphs_path, html=True), name="files")
main_api.mount("/export", StaticFiles(directory=export_path, html=True), name="export")
main_api.mount("/", StaticFiles(directory=site, html=True), name="site")

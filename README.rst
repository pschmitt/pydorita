pydorita
============

This library provides Python bindings for the iRobot Roomba 980 REST gateway
from https://github.com/koalazak/rest980

Example
--------------
.. code:: python

    from pydorita import PyDoritaClient
    # Connect to the REST980 gateway
    pd = PyDoritaClient(
        hostname='rest980-gw.lan',
        port=3000,
        username='roomba',
        password='R0mB!'
    )
    # Get the current state (ie. "run", "stuck" etc.)
    pd.phase
    # Get the current error code
    pd.error
    # Get the current battery percentage
    pd.battery
    # Get the current position
    pd.position
    # Start cleaning
    pd.clean()
    # Stop and dock
    pd.stop_and_dock()

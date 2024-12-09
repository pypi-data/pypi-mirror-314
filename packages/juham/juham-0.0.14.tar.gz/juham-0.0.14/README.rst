Welcome to Juham™ - Juha's Ultimate Home Automation Masterpiece
===============================================================

Project Status
--------------

**Current State**: **Pre-Alpha (Status 2)**  
In its current form, Juham™ may still resemble more of a home automation experiment (or even a "mess") than 
a "masterpiece," but I'm actively developing it to reach that goal!

Please check out the `CHANGELOG <CHANGELOG.rst>`_ file for changes in this release.


Goals
-----

The aim of Juham™ is to develop a robust home automation framework capable of controlling all the devices 
in my home, with the potential to be adapted for other homes as well.


Getting Started
---------------

### Installation

1. Install Juham™ core functionality:

   .. code-block:: bash

      pip install juham

   This will install the basic framework needed to get started.

2. Explore the available features and install any additional modules you require. For example, to add weather 
   forecasting plugins:

   .. code-block:: bash

      pip install juham_visualcrossing
      pip install juham_openweathermap

3. Set up **InfluxDB 3.0** and **Grafana Cloud**.  
   These services are optional, but I strongly recommend using them to monitor your home remotely. Juham™ 
   can function without them, but visualizing and recording data greatly enhances the system's capabilities.

4. Configure Juham™. This involves a two-step process:

   **Step 1:** Initialize the configuration by running:

   .. code-block:: bash

      juham --init

   This will generate JSON configuration files in your home directory at ``~/.juham/config/*``.

   **Step 2:** Edit the following configuration files to fit your setup:

   - ``Base.json``: Provide your MQTT host and port information.
   - ``JDatabase.json``: Enter your InfluxDB account details.
   - ``RVisualCrossing.json``: Add your Visual Crossing API key for weather forecasts.
   - ``Shelly*.json``: If you have Shelly devices, configure them here.

5. Perform a test run of Juham™ without the ``--init`` argument to check for any errors:

   .. code-block:: bash

      juham

6. If the system runs smoothly, you can set up ``juham`` as a service to run continuously.


Tailoring to Your Home
----------------------

Every home is unique, and Juham™ serves as a customizable starting point for building your own home automation system.


Special Thanks
--------------

This project would not have been possible without the generous support of two exceptional 
individuals: my friend, **Teppo K.**, and my son, **Mahi**. 

- Teppo provided the initial spark for this project by donating a Raspberry Pi, a temperature sensor, and an inspiring demonstration of his own home automation system.
- My son Mahi has been instrumental in translating my ideas into Python code, offering invaluable support and encouragement throughout the development process.

I am deeply grateful to both of you — thank you!

Masterpiece™  (**Development Status 2 - Pre-Alpha**)
====================================================

Try to be Nice
--------------

Welcome to **Masterpiece™** - Quite a Piece of Work!

Masterpiece™ is a **Python framework** designed for creating modular, scalable, plugin-aware, multi-threaded, and 
object-oriented applications with a hierarchical structure.

The name 'Masterpiece' was chosen to reflect a commitment to fine-grained modular design, with a touch of humor.




Goals
-----

Have fun while learning the Python ecosystem! The ultimate enjoyment, with a sprinkling of practicality, will be 
achieved by cranking the Fun-O-Meter™ up to 11. Coding should feel like a rollercoaster ride—minus the screaming 
and the long lines.

* **Pythonic Purity:**: Designed with strict adherence to Python conventions, ensuring idiomatic, readable, and maintainable code.
* **First-Time Excellence**: A framework that's reliable, correct, and efficient from the start, 
  and fun—because what’s a framework without a little joy?
* **Completeness**: A minimal yet robust API providing developers with total control over everything.
* **Productivity**: Reusable code to achieve maximum functionality with a minimal amount of code (read: money),
  and productivity increaseing with the size of the project. 

If you appreciate these design concepts, look no further; you've come to the right place! 


Project Status and Current State
--------------------------------

Here’s what is currently available:

* **Bug-Free Status**: Absolutely bug-free — just kidding! There are no known bugs remaining, as far as I can tell.
* **Wiki:** First Wiki pages under construction `Masterpiece Wiki <https://gitlab.com/juham/masterpiece/-/wikis/home>`_ 
* **Tutorial**: First tutorial `tutorial <docs/source/tutorial.rst>`_  to help you to get started with writing masterpieces. 
* **Package Infrastructure**: The basic Python package setup is finalized and configured with `pyproject.toml`.
* **Classes**: The existing classes have been finalized. 
* **Example Application**: The example application `examples/myhome.py` prints out its instance structure when run. 
  Despite its simplicity, it demonstrates the structure of a typical scalable and fully configurable software.
* **Plugin Projects**: Several plugin projects, e.g. `masterpiece_plugin` that plugs in a "Hello World" greeting to 
  `myhome.py`, demonstrating a minimal yet fully functional plugin.


What is currently not there yet:

* **Threads:**  This will be the focus of the next milestone. While multi-threading in Python might make some 
  developers raise an eyebrow due to the well-known Global Interpreter Lock (GIL), I trust the Python community 
  will continue to address these concerns. 

* **MQTT:**: This will also be a priority for the next milestone. The goal is for MasterPiece objects to 
  communicate seamlessly with each other using the MQTT protocol, enabling efficient message passing in 
  distributed environments.

* **User Interface:**: Instead of reinventing the wheel, Grafana will be the first choice for visualization 
  and user interaction. Grafana’s powerful and flexible interface will streamline the development process while 
  providing users with a robust, ready-made solution.


Projects
--------

Masterpiece comes in four Python projects:

1. **Masterpiece (core framework)**:  
   This is the core framework for building plugin-aware, multi-threaded applications. It includes a simple yet 
   fully functional application to help you get started and serves as a plugin-aware reference application 
   that can be scaled up to any size.

2. **Masterpiece Plugin (plugin example)**:  
   This is a basic plugin example that demonstrates how to create third-party plugins for applications built 
   using Masterpiece. It’s as simple as saying **"Hello, World!"**, literally.

3. **Masterpiece XML Format plugin:**:  
   This is a complete plugin example that demonstrates how to add new serialization format to
   Masterpiece. 

4. **Masterpiece Yaml Format plugin:**:  
   Another format plugin. Adds Yaml support to Masterpiece.


**Note**: This project contains only the core framework. The plugins are provided as a separate projects:

* `masterpiece_plugin <https://gitlab.com/juham/masterpiece_plugin>`_ .
* `masterpiece_xmlformat <https://gitlab.com/juham/masterpiece_xmlformat>`_.
* `masterpiece_yamlformat <https://gitlab.com/juham/masterpiece_yamlformat>`_.



Installing Masterpiece
----------------------

**Step 1**: Install Masterpiece and run the example application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install the core framework:

.. code-block:: bash

    pip install masterpiece

Then, navigate to the example folder and run the application:

.. code-block:: bash

    python examples/myhome.py

The application will print out its instance hierarchy. This is a simple example application to demonstrate the
basic structure of any multi-threaded, plugin-based, scalable MasterPiece applications.

**Example output**:

.. code-block:: text

    home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        └─ garage
            └─ EV charger

**Step 2**: Install the Masterpiece Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To extend the application with the **masterpiece_plugin**:

.. code-block:: bash

    pip install masterpiece_plugin

Run the application again:

.. code-block:: bash

    python examples/myhome.py

You'll now see a new object in the instance hierarchy, along with a friendly "Hello, World!" object.

**Example output**:

.. code-block:: text

    home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        ├─ garage
        │   └─ EV charger
        └─ Hello World - A Plugin

**Step 3**: Configurating
^^^^^^^^^^^^^^^^^^^^^^^^^

The application also demonstrates the usage of startup arguments. Run the application again:

.. code-block:: text

    examples/myhome.py --init --solar 10 --color red

and new 'Solar plant 10 kW' object appears in the tree.

- The ``--init`` argument tells the application to save its current configuration to a configuration files. 
- The ``--solar`` argument creates an instance of a solar power plant with a specified peak power of 10 kW.
- The ``--color`` argument can be used for setting the color for the tree diagram.

The above class properties (and many more) can also be defined in the class configuration files. By default, 
the configuration files are created in the ``~/.myhome/config`` folder, as determined by the ``application identifier`` 
and ``--config [anyname]``.

For example, ``--config temp`` will use the configuration files stored in the ``~/.myhome/temp/`` 
folder.


What's next
-----------

Congratulations! You've successfully installed Masterpiece, extended it with a plugin, and explored its configuration system. 
But what is all this for? 

That part is up to your imagination. Here's what you can explore next:

- Write Plugins: Develop your own plugins to extend Masterpiece with domain-specific functionality.
  Use the masterpiece_plugin as a starting point for inspiration.

- Leverage Configurations: Take advantage of configuration files to fine-tune your application's behavior 
  without changing the code. Experiment with the --config argument to manage multiple configurations for 
  different scenarios.

- Design a Custom Application: Build a unique application that fits your needs by combining existing plugins, 
  creating new objects in the instance hierarchy, and integrating external services or data sources.

- Contribute to the Community: Share your plugins or improvements with the Masterpiece community. 

Masterpiece provides the building blocks. Where you go from here is entirely up to you. Happy coding!


Contributing
------------

Please check out the `Masterpiece Issue Board <https://gitlab.com/juham/masterpiece/-/boards>`_ for tracking progress 
and tasks.


Developer Documentation
-----------------------

For full documentation and usage details, see the full documentation at `Documentation Index <docs/build/html/index.html>`_ 
(The docs may look rough; I’m still unraveling Sphinx's mysteries).


Special Thanks
--------------

Big thanks to the generous support of [Mahi.fi](https://mahi.fi) for helping bring this framework to life.

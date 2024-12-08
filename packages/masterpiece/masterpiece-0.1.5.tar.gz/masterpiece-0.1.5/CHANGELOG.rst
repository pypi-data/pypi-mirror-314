CHANGELOG
=========

[0.1.4]  17.12.2024
-------------------

**stable-0.1.4:** New stable release with minor improvements and bug fixes:

- **Type-hinting:** completed and `py.typed` file added to indicate 
  that the package supports PEP 561 type hints.

- **PluginManager:** The `add()` method of the `Composite` class now accepts `None` as
  a parameter. In such cases, it raises a `ValueException`.
  For example, calling `self.add(self.instantiate_plugin_by_name("SomePlugin"))` will
  now properly terminate the application if the plugin is not installed.

- **@override:** decorator imported from `typing_extensions` rather than from `typing`,
  for Python 3.9 backward compatibility. 

- **YamlFormat:** The YAML serialization format functionality has been removed from the core framework 
  and implemented as a separate plugin project, `masterpiece_yaml`.

- **Traversing the hierarchy:**:

  `URL` class: A new class for instance name-based identification of objects within hierarchical 
    tree structures.

  `make_url()` Method: Generates hierarchical paths for any object in the instance hierarchy.

  `resolve_url()` Method: Locates objects by their URL.

- **print():** method visualizing the instance hierarchy moved from the `example/myapp.py`to 
  `application.py` base class. Originally initiated as a demonstrative piece of code, but 
   turned out to be valueble feature for any MasterPiece application.


[0.1.3] - 4.11.2024
-------------------

- **stable-0.1.3:** First release tagged with `stable` prefix. When a Git tag is prefixed
  with stable, the masterpiece CD/CI pipeline deploys the package to the PyPI repository.

- **Development Status :: 2 - Pre-Alpha:** PyPi classifier elevated from Planning to Pre-Alpha


[0.1.0] - 3.11.2024
-------------------

- **Version elevated to 0.1.0:** The plugin API has been successfully tested with two separate plugins 
  and confirmed to work. Hooray!

- **classattrs_to_dict():** Who knew iterating over class attributes in Python could be so tricky? 
  Fixed—yes, really!


[0.0.9] - 2.11.2024
-------------------
- **Tutorial:** - Exceptionally well written world-class `tutorial <docs/source/tutorial.rst>`_
  covering the basics and essential features, I hope.

- **Bug Fixes:** 
  - PlugMaster class attempted to instantiate classes not subclassed from the Plugin class. 
  - Exception when issubclass() was called with class that was not registered.
  - several bugs fixed in both load_configuration() and save_configuration().
  - save_configuration() failed to save because it opened the file for reading, fixed.
  - is_abstract() class method removed, use inspect.isabstract() instead.


[0.0.7] - 1st 11.2024
---------------------

- **Milestone Achieved**: Despite the modest version increment, this release 
  brings substantial structural, architectural, and functional improvements. 
  With the release of version 0.0.7, I’ve completed my first two major milestones 
  for the project — definitely a cause for celebration!

- **Directory Structure Finalized**: Removed the ``core`` directory; all
  classes are now organized under ``masterpiece/masterpiece/*.py``.
  (Feeling like I’m evolving from a C++ boomer to a proper Pythonista!)

- **@classproperty**: A decorator class implemented as a replacement 
  for Python's decision to deprecate the combination of ``@classmethod`` and 
  ``@property``. This decorator addresses the fundamental principle of object-oriented 
  programming: any software is essentially composed of code and data (attributes 
  and methods), which can be either class-specific or instance-specific. Given this, 
  it is logical to have `@property` for instance-specific attributes and 
  `@classproperty` for class-specific attributes.

- **Serialization API Finalized**: Decoupled hard-coded JSON serialization,
  implementing it as a separate ``JsonFormat`` class. This is the default
  serialization format for the ``Application`` class decoupling also the format
  from the stream: any data can be formatted to any stream.

- **YamlFormat Added**: Implemented YAML serialization format, which can be selected
  with the startup option ``--application_serialization_form YamlFormat``.

- **Logging Improved**: Supports both class and instance methods, enabling
  both ``Foo.log_error(...)`` and ``foo.error(...)`` syntax.

- **Unit Tests Enhanced**: Coverage significantly improved, now reaching
  approximately 90%.



[0.0.6] - 26.10.2024
--------------------

- **Code and Data Decoupling**: Hardcoded `print()` methods have been removed
  from core classes and re-implemented using the new `do()` method.

- **ArgMaestro**: A class for fully automated class attribute initialization
  through startup arguments. Allows any public class attribute to be
  initialized using the `--classname_attributename [value]` convention.
  The class name is admittedly ridiculous, consider changing it.

- **Unit Test Coverage Improved**: Unit tests have been enhanced to a level
  where they provide meaningful test coverage.

- **Logging Typos Fixed**: All strings have been proofread and typos corrected.


[0.0.5] - 20.10.2024
--------------------

- **New startup argument --init**: If given, all classes in the application
  will create configuration files for their class attributes, if those files
  don't already exist. These configuration files allow users to define custom
  values for all public class attributes.

- **Rotating Logs**: The FileHandler has been replaced with
  TimedRotatingFileHandler, initialized with parameters `when='midnight'`,
  `interval=1`, and `backupCount=7` to rotate the log file daily and keep 7
  backup files. This change resolves the issue of log files growing
  indefinitely, which could eventually lead to the system running out of
  disk space.

- **Documentation Refactored**: All .rst files have been moved from Sphinx's
  docs/source directory to the project root folder for GitLab compatibility.

- **Time Functions**: The methods `epoc2utc()`, `timestamp()`, `epoc2utc()`
  and a few others removed. These were not actually methods of the Masterpiece
  class since they did not require any instance attributes. More importantly,
  this change aims to keep the Masterpiece framework focused on its core
  functionality.


[0.0.4] - October 18, 2024
--------------------------

- **MasterPiece**: Undefined class attribute `_class_id`, added.
- **MetaMasterPiece Refactored**: Replaced with a more lightweight
  `__init_subclass__()` solution, with special thanks to Mahi for his
  contribution.
- **Plugin Class Abstracted**: The plugin class is now subclassed from `ABC`
  to formally implement an abstract base class.
- **Pylint Warnings Resolved**: Fixed issues such as long lines, which have
  been split for better readability.
- **Docstrings Improved**: Added more comprehensive documentation with a
  professional tone for several methods.


[0.0.3] - October 12, 2024
--------------------------

- **From C++ boomer to Python professional**: Directory structure simplified:

  - `src` folder removed
  - `masterpiece/base` folder renamed to `masterpiece/core`
  - `plugins` folder moved outside the project, will be implemented as a
    separate project (one project - one repository principle)
  - Minor additions and improvements to Docstrings.


[0.0.2] - October 10, 2024
--------------------------

- **GitLab Ready**: Revised documentation tone slightly to reflect a more
  professional and serious nature. Removed excessive humor that may have
  detracted from the perceived professionalism of the toolkit.


[0.0.1] - August 4, 2024
------------------------

Pip release with Python pip package uploaded.

New Features and Improvements:

- **Trademark**: Cool (not?) slogan: Masterpiece - Quite a piece of work
- **Plugin API**: Enhanced the plugin API with two classes: `Plugin` and
  `PlugMaster` with compatibility with Python versions 3.8 and later.
  The most recent version tested is 3.12.
- **Meta-Class Automation**: Per-class bureaucracy automated using Python's
  meta-class concept.
- **Folder Structure**: Redesigned for future expansion. There is now separate
  root folders for core and plugin modules.
- **Base Class**: Added new base class for MasterPiece applications in
  `base/application.py`.
- **Example Application**: Added `examples/myhome.py` to demonstrate the
  general structure of MasterPiece applications.
- **Startup Argument Parsing**: Added API for parsing startup arguments.
- **Serialization API**: Fully featured serialization with backward
  compatibility support implemented.
- **Documentation**: Added comprehensive docstrings to numerous classes,
  aiming for fully documented professional Python code.
- **Type Annotations**: Added type annotations to numerous previously
  non-typed method arguments, moving towards a fully typed Python code.
- **Sphinx conf.py**: Created default Sphinx `conf.py` file in the
  `masterpiece/sphinx` folder.
- **Bug Fixes and Improvements**:

  - Added `encoding="utf-8"` to `open()` calls
  - Added `exclude __pycache__` to MANIFEST.in, to avoid including the folders
    with the setup.


[0.0.0] - May 31, 2024
----------------------

Initial, private release (minimal set of classes unified from the RTE and
JUHAM Python applications).

- **Base Class Draft**: Initial version of the `MasterPiece` and `Composite`
  classes.
- **Python Packaging**: Python package infrastructure setup using
  `pyproject.toml`, installable via pip.
- **Documentation**:

  - Added LICENSE, README, and other standard files in .rst format.
  - Developer documentation autogenerated with Sphinx toolset. Support for
    Doxygen dropped.
- **Project Name**: Named the project 'MasterPiece™', with a note that 'M'
  currently stands for mission rather than masterpiece.
- **Miscellaneous**: Some unconventional use of the Python programming
  language.

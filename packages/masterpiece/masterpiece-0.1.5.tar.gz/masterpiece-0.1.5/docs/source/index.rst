Welcome to MasterPiece documentation!
=====================================

.. image:: _static/masterpiece.png
    :alt: Masterpiece - A Piece of Work
    :width: 400px
    :height: 300px

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   masterpiece/index

.. include:: ../../README.rst

.. include:: ../../LICENSE.rst

.. include:: ../../CONTRIBUTING.rst

.. include:: ../../CHANGELOG.rst

.. include:: ../../TODO.rst



Classes
-------

.. inheritance-diagram:: masterpiece.masterpiece 
    masterpiece.composite.Composite 
    masterpiece.application.Application 
    masterpiece.plugin.Plugin 
    masterpiece.plugmaster.PlugMaster 
    masterpiece.argmaestro.ArgMaestro 
    masterpiece.log.Log 
    masterpiece.treevisualizer.TreeVisualizer
   :parts: 1



Instances
---------

Instances of these classes can be grouped into hierarchical structure to model real world apparatuses.


Instance Diagram
----------------

(Just a test to play with mermaid)

.. mermaid::

   classDiagram
       class MainCompositeObject {
           MasterPiece1: MasterPiece
           SubCompositeObject: SubCompositeObject
       }
       class SubCompositeObject {
           SubMasterPiece1: MasterPiece
           SubMasterPiece2: MasterPiece
       }
       MainCompositeObject --> MasterPiece1 : contains
       MainCompositeObject --> SubCompositeObject : contains
       SubCompositeObject --> SubMasterPiece1 : contains
       SubCompositeObject --> SubMasterPiece2 : contains


Index
=====

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

XML Serialization Format
========================

This project implements the `masterpiece_xmlformat` Python package to add XML support to `masterpiece` 
applications.

Usage
-----

To install:

.. code-block:: bash
  
  pip install masterpiece_xmlformat

Once installed, you can pass the `--init` and `--application_serialization_format` 
startup arguments to create a default set of configuration files. For example, to create 
XML configuration files for the 'examples/myapp.py' application:

.. code-block:: bash

  mkdir -p ~/.myhome/config
  python examples/myhome.py --init --application_serialization_format XMLFormat

Upon successful execution, there should be a file located at `~/.myhome/config/MyHome.xml` 
with the following content:

.. code-block:: xml

  <?xml version='1.0' encoding='utf-8'?>
  <MyHome>
    <solar>0.0</solar>
    <color>yellow</color>
  </MyHome>

To use XML as the default format, add the following line of code to your application:

.. code-block:: python

  Application.serialization_format = "XMLFormat"

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

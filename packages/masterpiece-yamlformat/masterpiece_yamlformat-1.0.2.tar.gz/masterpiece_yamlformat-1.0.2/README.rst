Yaml Serialization Format
=========================

The native serialization format for `masterpiece` is **Json**. However, any serialization format
can be plugged in.

This project implements the `masterpiece_yamlformat` Python package to add **Yaml** support to `masterpiece` 
applications.

Usage
-----

To install:

.. code-block:: bash

  pip install masterpiece_yamlformat

Once installed, you can pass the `--init` and `--application_serialization_format` 
startup arguments to create a default set of configuration files. For example, to create 
yaml configuration files for the 'examples/myapp.py' application:

.. code-block:: bash

  mkdir -p ~/.myhome/config
  python examples/myhome.py --init --application_serialization_format YamlFormat

Upon successful execution, there should be a file located at `~/.myhome/config/MyHome.yaml`.

To use yaml as the default format, add the following line of code to your application:

.. code-block:: python

  Application.serialization_format = "YamlFormat"

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

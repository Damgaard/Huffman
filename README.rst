Huffman
=======

Handles the lossless Huffman compression. Both encoding and decoding.

Dependencies
------------

This package has the ``bitstring`` and ``docopt`` libraries as a dependency.
Install with ``pip``.

.. code-block:: bash

   $ pip install bitstring docopt

Usage
-----

3 public functions are exposed. ``encode``, ``decode`` and ``build_tree``.
When decoding and encoding a file, a Huffman tree is needed. Such a tree can
be generated with the ``build_tree`` function from a string. The tree is
stored in a ``NamedTuple`` data structure.

``encode`` encodes a string to a path. Either using the optimal huffman tree
to encode the string, alternatively if the ``tree`` argument is given, this
tree will be used. This gives the option of using a single tree to encode
multiple file with the same encoding, even if it isn't optimal for all files.
The tree used is returned from this function. The big downside is that files
cannot be decoded without the huffman tree. Remember to store the tree
somewhere if you want to decode the file later.

``decode`` takes a file and a tree and decodes the huffman encoded file using
the tree. The decoded content is returned.

More information about the 3 functions are stored in their docstrings and can
be retrieved either by reading the source or using the builtin ``help``
function.

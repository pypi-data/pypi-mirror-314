=============
API Reference
=============

Base classes
============

.. autoclass:: TextVault.Encryptor
    :members:
    :undoc-members:
    :member-order: bysource

.. autoclass:: TextVault.Key
    :members:
    :special-members: __init__, __repr__
    :undoc-members:
    :member-order: bysource

-------------------------------------------

.. _kanpsack_api:

Knapsack Encryption Module
==========================

:ref:`Usage <knapsack_usage>`

.. autoclass:: TextVault.KnapsackEncryptor
    :members:
    :member-order: bysource
.. autoclass:: TextVault.KnapsackKey
    :members:
    :member-order: bysource

**Example**

.. code-block:: python

    # After installing TextVault

    from TextVault import KnapsackEncryptor, KnapsackKey
    txt = "Hello, World! 😀"
    enc = KnapsackEncryptor()

    pub, priv = enc.newkey()
    encrypted = enc.encrypt(txt, pub)
    decrypted = enc.decrypt(encrypted, priv)

    print("Public key:", pub)
    print("Private key:", priv)
    print()

    print("Original:", txt)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print()

    pub.export_txt("knap_public_key.txt")
    pub_2 = KnapsackKey.import_txt("knap_public_key.txt")

    print("Original Key:", pub)
    print("After Save & Load:", pub_2)

----------------------------------------------

RSA Encryption Module
=====================
.. autoclass:: TextVault.RsaEncryptor
    :members:
    :undoc-members:
    :member-order: bysource

----------------------------------------------

Vigenère Encryption Module
==========================
.. autoclass:: TextVault.VigenereEncryptor
    :members:
    :undoc-members:
    :member-order: bysource

----------------------------------------------

JMatrix Encryption Module
==========================
.. autoclass:: TextVault.JMatrixEncryptor
    :members:
    :undoc-members:
    :member-order: bysource
.. autoclass:: TextVault.JMatrixKey
    :members:
    :undoc-members:
    :member-order: bysource

-----------------------------------------------

HillCipherWithNumbers Module
============================
.. autoclass:: TextVault.Hillcipherwithnumbers
    :members:
    :undoc-members:
    :member-order: bysource

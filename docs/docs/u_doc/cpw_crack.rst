
Cisco type 7 passwords Encryption/Decryption
============================================

Activities that can be done are:
	* Encrypt/Decrypt plain-text password string v/s Cisco type-7 encrypted string 
	* Decrypt all type-7 passwords from cisco configuration. (create a new file)
	* Mask all type-7, type-9 passwords from cisco configuration. (create a new file)


-----


Password encrypt
------------------

**Steps Involved:**

	* Import the ``encrypt_type7()`` function from ``nettoolkit``.
	* Pass plain-text-password as string argument for the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import encrypt_type7
		>>> encrypt_type7("Cisco1234")
		'062506324f41584b5643'				## Encrypted password string.



Password decrypt
-------------------------------

**Steps Involved:**

	* Import the ``decrypt_type7()`` function from ``nettoolkit``.
	* Pass plain-text-password as string argument for the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import decrypt_type7
		>>> decrypt_type7("062506324f41584b5643")
		'Cisco1234'			## Decrypted password string


-----


Decrypt type7 passwords from cisco configuration file
------------------------------------------------------

**Steps Involved:**

	* Import the ``decrypt_file_passwords`` function from ``nettoolkit``
	* First argument for the function is cisco configuration file name
	* Second argument for the function is new output file name
	* Output file will have all type-7 passwords decrypted

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import decrypt_file_passwords
		>>> decrypt_file_passwords("input_file.log", "output_file.log")



Mask type7 passwords from cisco configuration file
---------------------------------------------------

**Steps Involved:**

	* Import the ``mask_file_passwords`` function from ``nettoolkit``
	* First argument for the function is cisco configuration file name
	* Second argument for the function is new output file name
	* Output file will have all type7 and type9 password masked

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import mask_file_passwords
		>>> mask_file_passwords("input_file.log", "output_file.log")


-----


.. note::
		
	These features are available in the package >= 0.0.14


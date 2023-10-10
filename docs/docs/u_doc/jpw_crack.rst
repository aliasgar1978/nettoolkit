
Juniper $9 passwords Encryption/Decryption
============================================

Activities that can be done are:
	* Encrypt/Decrypt plain-text password string v/s Juniper $9$ encrypted string 
	* Decrypt all $9$ passwords from juniper configuration. (creates a new file)
	* Mask all $9$ passwords from juniper configuration. (creates a new file)

-----


Password encrypt
------------------

**Steps Involved:**

	* Import the ``juniper_encrypt()`` function from ``nettoolkit``.
	* Pass plain-text-password as string argument for the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import juniper_encrypt
		>>> juniper_encrypt("welcome1234")
		'$9$DDk5FCA0Rhrmf0IEyW8-VwYaZDikPTzji'				## Encrypted password string.



Password decrypt
-------------------------------

**Steps Involved:**

	* Import the ``juniper_decrypt()`` function from ``nettoolkit``.
	* Pass encrypted string as argument for the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import juniper_decrypt
		>>> juniper_decrypt("$9$DDk5FCA0Rhrmf0IEyW8-VwYaZDikPTzji")
		'welcome1234'			## Decrypted password string


-----


Decrypt all $9 passwords from Juniper configuration file
---------------------------------------------------------

**Steps Involved:**

	* Import the ``decrypt_doller9_file_passwords`` function from ``nettoolkit``
	* First argument for the function is juniper configuration file name
	* Second argument for the function is new output file name
	* Output file will have all $9$ passwords decrypted

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import decrypt_doller9_file_passwords
		>>> decrypt_doller9_file_passwords("input_file.log", "output_file.log")



Mask all $9 passwords from juniper configuration file
-----------------------------------------------------

**Steps Involved:**

	* Import the ``mask_doller9_file_passwords`` function from ``nettoolkit``
	* First argument for the function is cisco configuration file name
	* Second argument for the function is new output file name
	* Output file will have all $9$ password masked

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import mask_doller9_file_passwords
		>>> mask_doller9_file_passwords("input_file.log", "output_file.log")


-----


.. note::
		
	Refer Version Control log to see the version from where these features are made available.


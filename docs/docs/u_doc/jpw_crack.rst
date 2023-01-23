
Juniper $9 passwords Encryption/Decryption
============================================

Activities that can be done are:
	* Encrypt/Decrypt plain-text password string v/s Juniper $9 encrypted string 


Encrypt to $9:
------------------

**Steps Involved:**

	* Import the ``juniper_encrypt()`` function from ``nettoolkit``.
	* Pass plain-text-password as string argument for the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import juniper_encrypt
		>>> juniper_encrypt("welcome1234")
		'$9$DDk5FCA0Rhrmf0IEyW8-VwYaZDikPTzji'				## Encrypted password string.


Decrypt Juniper $9 password:
-------------------------------

**Steps Involved:**

	* Import the ``juniper_decrypt()`` function from ``nettoolkit``.
	* Pass encrypted string as argument for the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import juniper_decrypt
		>>> juniper_decrypt("$9$DDk5FCA0Rhrmf0IEyW8-VwYaZDikPTzji")
		'welcome1234'			## Decrypted password string





.. note::
		
	This feature is made available from the package >= 0.0.17

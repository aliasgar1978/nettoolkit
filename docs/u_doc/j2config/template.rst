
Sample Jinja Template data to use with  j2config
======================================================

::


	! ---------------------------------------------------------------------------- !
	!   SAMPLE JINJA SECTION - TO DEFINE THE OBJECTS WITHIN TEMPLATE
	! ---------------------------------------------------------------------------- !

	{#- =========================================================================== -#}
							{#- DEFINE OBJECTS -#}
	{#- =========================================================================== -#}
	{% set Physical = table | Physical -%}




	! ---------------------------------------------------------------------------- !
	!   SAMPLE JINJA SECTION - TO GENERATING PHYSICAL INTERFACE CONFIGURATION
	! ---------------------------------------------------------------------------- !

	{% for data in Physical | sorted_interfaces -%}
	interface {{ data.interface }}
	description {{ data.description }}
	{% for vlan_group in data.vlan_members | str_to_list | groups_of_nine -%}
	{% if loop.index == 1 -%}
	switchport trunk allowed vlan {{ vlan_group | comma_separated }}
	{%- else -%}
	switchport trunk allowed vlan add {{ vlan_group | comma_separated }}
	{%- endif %}
	{% endfor -%}
	switchport mode trunk
	switchport nonegotiate
	{% if data.link_status.lower() in ('administratively down', 'disabled') -%}
	shutdown
	{%- else -%}
	no shutdown
	{%- endif %}
	!
	{% endfor -%}



	! ---------------------------------------------------------------------------- !
	!   SAMPLE JINJA SECTION - TO MODIFY ACL / var table customer_servers DATA
	! ---------------------------------------------------------------------------- !

	ip access-list standard 100
	10 remark /**********************************************
	20 remark Permitted servers for ACL 100
	30 remark **********************************************/
	{% for server in var.customer_servers | str_to_list -%}
	{{ (loop.index+3)*10 }} permit {{ server | nth_ip(0) }} {{ server | invmask }}
	{% endfor -%}
	9990 deny   any
	!
	logging host {{ var.syslog_server_1 }}
	logging host {{ var.syslog_server_2 }}	
	ntp server {{ var.ntp_server_1 }}
	ntp server {{ var.ntp_server_2 }}
	!

	! ---------------------------------------------------------------------------- !
	!  ... And Many More.. (Explore it by self)
	! ---------------------------------------------------------------------------- !



-----


.. admonition:: Notice

	* Make a note that output generates based on jinja template and template variables.
	* Make sure to cross-check the generated facts before using it.


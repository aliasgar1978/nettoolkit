

# ---------------------------------------------------------------------------------------
#   sets of event updator variables
# ---------------------------------------------------------------------------------------

MINITOOLS_EVENT_UPDATERS = {
}
IPSCANNER_EVENT_UPDATERS = {
}
CAPTUREIT_EVENT_UPDATERS = {
}
FACTSFINDER_EVENT_UPDATERS = {
}
J2CONFIG_EVENT_UPDATERS = {
}
PYVIG_EVENT_UPDATERS = {
}
CONFIGURE_EVENT_UPDATERS = {
	'lb_config_excel_files', 'lb_config_excel_files_sequenced'
}


# ---------------------------------------------------------------------------------------
EVENT_ITEM_UPDATORS = set()
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(MINITOOLS_EVENT_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(IPSCANNER_EVENT_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CAPTUREIT_EVENT_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(FACTSFINDER_EVENT_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(J2CONFIG_EVENT_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(PYVIG_EVENT_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CONFIGURE_EVENT_UPDATERS)		
# ---------------------------------------------------------------------------------------


__all__ = [EVENT_ITEM_UPDATORS]
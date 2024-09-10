
from nettoolkit.capture_it.forms.execs import CAPTUREIT_ITEM_UPDATERS
from nettoolkit.facts_finder.forms.execs import FACTSFINDER_ITEM_UPDATERS
from nettoolkit.j2config.forms.execs import J2CONFIG_ITEM_UPDATERS
from nettoolkit.pyVig.forms.execs import PYVIG_ITEM_UPDATERS

# ---------------------------------------------------------------------------------------
#   sets of event updator variables
# ---------------------------------------------------------------------------------------

MINITOOLS_ITEM_UPDATERS = {
}
IPSCANNER_ITEM_UPDATERS = {
}


# FACTSFINDER_ITEM_UPDATERS = {
# }
# J2CONFIG_ITEM_UPDATERS = {
# }
# PYVIG_ITEM_UPDATERS = {
# }
CONFIGURE_ITEM_UPDATERS = {
	'lb_config_excel_files', 'lb_config_excel_files_sequenced'
}


# ---------------------------------------------------------------------------------------
EVENT_ITEM_UPDATORS = set()
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(MINITOOLS_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(IPSCANNER_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CAPTUREIT_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(FACTSFINDER_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(J2CONFIG_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(PYVIG_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CONFIGURE_ITEM_UPDATERS)		
# ---------------------------------------------------------------------------------------


__all__ = [EVENT_ITEM_UPDATORS]
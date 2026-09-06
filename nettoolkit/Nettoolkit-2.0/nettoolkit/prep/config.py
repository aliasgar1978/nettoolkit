
from dataclasses import dataclass, field
from jinja2 import Environment, FileSystemLoader
from inspect import getmembers, isfunction, isclass, isroutine
import os

from nettoolkit.cmn.fio import read_yaml, write_to_file

from .read_conditions import verify_jinja_syntax_sanity
from .cmn import common_fn as cmn

# =======================================================================================================
@dataclass
class Render_Config():
    """boiler plate code class for start configuration preparation
    """	
    jinja_template_file: str

    # -----------------------------------------
    # IMPORT FILTERS FOR JINJA VARIABLES
    # -----------------------------------------
    filters: dict = field(default_factory=dict)

    def __post_init__(self):
        self.jinja_sanity_check()
        try:
            self.filters.update(dict(getmembers(cmn, isfunction)))
        except: pass
        self.output_text = ''

    # filters.update({'Vrf': Vrf, 'Bgp': Bgp,
    # 	'Vlan': Vlan, 'Physical': Physical, 'Aggregated': Aggregated, 'Loopback': Loopback, 		
    # 	'Ospf': Ospf, 'Static': Static,
    # })
    # filters.update(dict(getmembers(Vrf, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Vlan, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Physical, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Bgp, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Aggregated, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Loopback, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Static, lambda x:not(isroutine(x))))['__dict__'] )
    # filters.update(dict(getmembers(Ospf, lambda x:not(isroutine(x))))['__dict__'] )

    def jinja_sanity_check(self):
        syntax_check = verify_jinja_syntax_sanity(self.jinja_template_file)
        if not syntax_check['is_valid']:
            # Format a clear, indented error report summarizing all template defects
            error_summary = "\n".join(f"  -> {err}" for err in syntax_check['errors'])
            raise ValueError(
                f"\n[-] Render Engine Initialization Aborted!\n"
                f"[-] Template File '{self.jinja_template_file}' has syntax errors:\n"
                f"{error_summary}\n"
                f"[-] Please correct these blocks before re-running the configuration engine."
            )



    def add_custom_class_as_filter(self, **kwargs):
        """add custom classes and its methods as jinja filters. External callable.
        """
        for filtername, _cls in kwargs.items():
            try:
                self.filters.update({filtername: _cls})
                class_members = dict(getmembers(_cls, lambda x: not isroutine(x)))
                if '__dict__' in class_members:
                    # Safely isolate pure properties if an underlying proxy map exists
                    try:
                        self.filters.update(dict(class_members['__dict__']))
                    except Exception:
                        pass
                else:
                    self.filters.update(class_members)

            except Exception as e:
                raise Exception(f"[-] Class Insertion Failed for filter {filtername}\n{e}")

    def add_custom_module_methods_as_filters(self, module):
        try:
            self.filters.update(dict(getmembers(module, isfunction)))
        except Exception as e:
            raise Exception(f"[-] Module Insertion Failed for module context {module}\n{e}")


    def start(self, **databases):
        """kick start generation
        """
        # ## LOAD - DATA
        resolved_databases = self.get_resolved_databases(**databases)

        # ## LOAD - JINJA TEMPLATE AND ENVIRONMENT
        templateLoader = FileSystemLoader(searchpath='')
        templateEnv = Environment(
            loader=templateLoader, 
            extensions=['jinja2.ext.loopcontrols', 'jinja2.ext.do',]
        )

        # Inject unified multi-vendor/custom filters map block directly into the context environment
        for key, value in self.filters.items():
            templateEnv.filters[key] = value

        # ## TEMPLATE FILE		
        template = templateEnv.get_template(self.jinja_template_file)
        self.output_text = template.render(**resolved_databases)#, undefined=jinja2.StrictUndefined) # Enable undefined for strict variable check


    def get_resolved_databases(self, **databases):
        resolved_databases = {}
        for db_key, db_source in databases.items():
            
            # Scenario A: If it's already a dictionary, it's pre-parsed memory data. Map it directly!
            if isinstance(db_source, dict):
                resolved_databases[db_key] = db_source
                continue

            # Scenario B: If it's a string, we MUST explicitly confirm it is a valid YAML file path
            elif isinstance(db_source, str):
                # 1. Verification Step: Check if the path string exists physically on disk
                if not os.path.isfile(db_source):
                    raise FileNotFoundError(
                        f"[-] Render Engine Error: The source path provided for database key '{db_key}' "
                        f"does not exist or is not a file: '{db_source}'"
                    )
                
                # 2. Verification Step: Enforce file extension type sanity checks
                if not (db_source.lower().endswith('.yaml') or db_source.lower().endswith('.yml')):
                    raise ValueError(
                        f"[-] Render Engine Error: File validation mismatch for key '{db_key}'. "
                        f"Expected a YAML file layout, but got: '{db_source}'"
                    )

                # 3. Execution Step: Read the file securely using your utility tool
                try:
                    parsed_content = read_yaml(db_source)
                except Exception as e:
                    raise Exception(
                        f"[-] Render Engine Error: Failed to execute read_yaml on file '{db_source}' "
                        f"for database key '{db_key}'. Underloaded error track:\n{e}"
                    )

                # 4. Verification Step: CONFIRM that the read operation returned a valid database dictionary!
                if not isinstance(parsed_content, dict):
                    # Handle cases where the file was completely empty or formatted as a flat list/string
                    raise TypeError(
                        f"[-] Render Engine Error: File '{db_source}' parsed successfully, "
                        f"but did not return a valid dictionary structure! Got: {type(parsed_content)}"
                    )

                # Complete the confirmation tracking registration safely
                resolved_databases[db_key] = parsed_content

            else:
                # Catch any bizarre data types passed by mistake (like lists, numbers, or objects)
                raise TypeError(
                    f"[-] Render Engine Error: Invalid input data type passed for key '{db_key}'. "
                    f"Must be either a file path string or a pre-parsed dictionary mapping block, "
                    f"got: {type(db_source)}"
                )
        return resolved_databases

    def write_to_file(self, file):
        write_to_file(file, self.output_text)


# =======================================================================================
# Main bypass
# =======================================================================================
if __name__ == "__main__": 
    pass
# =======================================================================================

__all__ = ['Render_Config', ]

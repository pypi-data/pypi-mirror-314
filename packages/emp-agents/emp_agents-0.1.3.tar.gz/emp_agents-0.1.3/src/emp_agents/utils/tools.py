import importlib.util
import pkgutil


def load_tools(directory: str):
    tools = []
    tools_map: dict = {}
    directory_import = directory.rstrip(".").replace("/", ".")
    for importer, pkg_name, is_pkg in pkgutil.iter_modules([directory]):
        if is_pkg:
            module = importlib.import_module(f"{directory_import}.{pkg_name}")
            try:
                tools.extend(module.TOOLS)
            except AttributeError:
                pass
            try:
                tools_map |= module.TOOL_MAP
            except AttributeError:
                pass
    return tools, tools_map

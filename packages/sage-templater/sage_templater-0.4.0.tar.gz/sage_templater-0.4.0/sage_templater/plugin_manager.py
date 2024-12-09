from typing import List

import pluggy

from sage_templater.schemas import SmallBoxRecordSchema

hookspec = pluggy.HookspecMarker("template_parser")
hookimpl = pluggy.HookimplMarker("template_parser")


class TemplateParserSpecs:
    @hookspec
    def parse_file(self: str) -> List[SmallBoxRecordSchema]:
        """Parse a file and return a list of SmallBoxRecordSchema."""
        pass


plugin_manager = pluggy.PluginManager("template_parser")
plugin_manager.add_hookspecs(TemplateParserSpecs)

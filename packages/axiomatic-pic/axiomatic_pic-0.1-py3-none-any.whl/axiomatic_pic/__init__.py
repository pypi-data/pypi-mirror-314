import os

import platformdirs
from axiomatic import Axiomatic
from IPython import get_ipython
from IPython.core.magic import register_line_cell_magic, register_line_magic
from IPython.display import HTML, display


class AXMagic:
    def __init__(self):
        self.folder = platformdirs.user_config_dir("axiomatic")
        if not os.path.exists(f"{self.folder}/api_key"):
            os.makedirs(self.folder)
            self.api_key = None
        else:
            with open(f"{self.folder}/api_key", "r") as f:
                self.api_key = f.read()
            self.ax = Axiomatic(api_key=self.api_key)

    def ax_api(self, query):
        folder = platformdirs.user_config_dir("axiomatic")
        with open(f"{folder}/api_key", "w") as f:
            f.write(query)
            self.api = query
            self.ax = Axiomatic(api_key=self.api)
            print("API key set.")

    def ax_query(self, query, cell=None):
        if self.api_key:
            result = self.ax.experimental.magic_request(query=query, cell=cell)

            get_ipython().set_next_input(f"{result.code}", replace=False)
            display(HTML(result.response))
        else:
            print(
                "Please set your Axiomatic API key first with the command %ax_api API_KEY. Request the api key at our Customer Service."
            )

    def ax_fix(self, query, cell=None):
        # Just dummy at the moment
        return self.ax_query(query, cell)


def load_ipython_extension(ipython):
    ax_magic = AXMagic()
    ipython.register_magic_function(ax_magic.ax_query, "line_cell")
    ipython.register_magic_function(ax_magic.ax_fix, "line_cell")
    ipython.register_magic_function(ax_magic.ax_api, "line")

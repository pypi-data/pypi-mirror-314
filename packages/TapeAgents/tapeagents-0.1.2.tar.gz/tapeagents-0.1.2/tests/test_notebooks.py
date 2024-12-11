import pathlib
import shutil
from pathlib import Path

import testbook
from make_test_data import run_test_in_tmp_dir

res_dir = f"{pathlib.Path(__file__).parent.resolve()}/res"


def test_intro_notebook():
    intro_notebook_path = Path("intro.ipynb").resolve()
    assets_path = Path("assets").resolve()
    with testbook.testbook(intro_notebook_path) as tb:
        with run_test_in_tmp_dir("intro_notebook"):
            shutil.copytree(assets_path, Path("assets"))
            tb.inject(
                f"""
                from tapeagents import llms
                llms._REPLAY_SQLITE = "{res_dir}/intro_notebook/tapedata.sqlite"
                from tapeagents.tools import simple_browser
                simple_browser._FORCE_CACHE_PATH = "{res_dir}/intro_notebook/web_cache.jsonl"
                from tapeagents.tools import tool_cache
                tool_cache._CACHE_PATH = "{res_dir}/intro_notebook/tool_cache.jsonl"
                tool_cache._FORCE_CACHE = True
                """,
                before=0,
            )
            tb.execute()

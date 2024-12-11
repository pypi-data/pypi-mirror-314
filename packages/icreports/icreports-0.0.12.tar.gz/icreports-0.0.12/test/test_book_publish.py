import shutil

from iccore.test_utils import get_test_data_dir, get_test_output_dir

from icreports.document.jupyter_book import toc as jb_toc
from icreports.document import config, toc
from icreports.rendering.context import RenderContext
from icreports.rendering.book import render


def test_book_publish():
    content_root = get_test_data_dir() / "mock_document"

    content = toc.load_content(content_root,
                               jb_toc.from_jupyterbook(
                                   jb_toc.read(content_root / "_toc.yml")))
    
    build_dir = get_test_output_dir()
    ctx = RenderContext(source_dir = content_root,
                        build_dir = build_dir,
                        config = config.read(content_root / "_config.yml"))

    render(content, ctx)

    shutil.rmtree(build_dir)

import logging
from pathlib import Path

from icreports.document import toc
from icreports.document.jupyter_book import toc as jb_toc
import icreports.document.config
from icreports.rendering import book, RenderContext

logger = logging.getLogger(__name__)


def render_book(source_dir: Path, build_dir: Path, config_path: Path, rebuild: bool):

    logger.info("Loading config from %s", config_path)
    config = icreports.document.config.read(config_path)

    toc_path = source_dir / "_toc.yml"
    logger.info("Reading toc from %s", toc_path)
    contents = toc.load_content(
        source_dir, jb_toc.from_jupyterbook(jb_toc.read(toc_path))
    )

    ctx = RenderContext(
        source_dir=source_dir,
        build_dir=build_dir,
        config=config,
        rebuild=rebuild,
    )
    book.render(contents, ctx)

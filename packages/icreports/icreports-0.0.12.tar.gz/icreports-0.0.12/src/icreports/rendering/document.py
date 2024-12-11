"""
Module to support rendering documents to disk for a given
build context
"""

import os
import shutil
import logging
from typing import Callable
from functools import partial

from iccore import filesystem as fs

import ictasks
from ictasks import Task

from icreports.document import toc, config
from icreports.rendering import media

from .context import RenderContext, replace_dirs

logger = logging.getLogger(__name__)


def _render_build(
    contents: toc.TableOfContents,
    ctx: RenderContext,
    build: config.Build,
    copy_sources_func: Callable,
    build_funcs: dict[str, Callable],
):

    logger.info("Start rendering build: %s", build.name)

    build_dir = ctx.build_dir / build.name
    fs.clear_dir(build_dir)

    logger.info("Copying source files")
    copy_sources_func(contents, ctx, build)

    logger.info("Copying media files")
    fs.copy_files(ctx.media_dir, build_dir / ctx.config.media_dir)
    fs.copy_files(ctx.media_build_dir, build_dir / ctx.config.media_dir)

    build_ctx = replace_dirs(ctx, build_dir)
    logger.info("Rendering with %s", build_ctx)

    if "src" in build.outputs:
        src_archive = build_dir / "src_archive"
        os.makedirs(src_archive, exist_ok=True)
        shutil.copytree(build_dir / "src", src_archive / "src")
        shutil.copy(build_dir / "_config.yml", src_archive)
        shutil.copy(build_dir / "_toc.yml", src_archive)

        fs.make_archive(
            build_ctx.build_dir / f"{ctx.config.project_name}_src",
            "zip",
            src_archive,
        )

        shutil.rmtree(src_archive)

    for fmt, func in build_funcs.items():
        if fmt in build.outputs:
            logger.info("Rendering format: %s", fmt)
            func(ctx.config.project_name, build_ctx)

    logger.info("Finished rendering build: %s", build.name)


def _task_func(render_func: Callable, _: Task):
    render_func()


def render(
    contents: toc.TableOfContents,
    ctx: RenderContext,
    copy_sources_func: Callable,
    build_funcs: dict[str, Callable],
):
    """
    Render a document to disk for a given render context. User provided callbacks are
    to copy book sources to the output archive and build functions for supported
    formats.

    Particular document types, such as Book, provide suitable callbacks for each.

    :param TableOfContents contents: The content to render
    :param RenderContext ctx: The settings for the render
    :param Callable copy_sources_func: Function to copy document source files to output
    :param dict[str, Callable] build_funcs: Function to build the document per format
    """

    logging.info("Rendering document with: %s", ctx)

    media.convert(ctx.media_dir, ctx.media_build_dir, ctx.conversion_dir)

    tasks = []
    for build in ctx.config.builds:
        render_func = partial(
            _render_build, contents, ctx, build, copy_sources_func, build_funcs
        )
        tasks.append(Task(launch_func=partial(_task_func, render_func)))
    ictasks.run_funcs(tasks)

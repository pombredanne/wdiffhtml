#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Some functions to generate HTMLifeied diffs with `wdiff`.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import subprocess as sub

from pathlib import Path

from .settings import (
  CMD_WDIFF,
  OPTIONS_LINEBREAK,
  OPTIONS_OUTPUT,
  TEMPLATE,
  CSS,
  JS,
)


__all__ = [
  'WdiffNotFoundError',
  'check_for_wdiff',
  'generate_wdiff',
  'build_paragraph',
  'wrap_paragraphs',
  'wrap_content',
]


class WdiffNotFoundError(Exception):
 """This exception is raised, if the `wdiff` command is not found."""


def check_for_wdiff():
  """
  Checks if the `wdiff` command can be found.

  Raises:

    WdiffNotFoundError: if ``wdiff`` is not found.

  """
  cmd = ['which', CMD_WDIFF]
  proc = sub.Popen(cmd, stdout=sub.DEVNULL)
  proc.wait()
  if proc.returncode != 0:
    msg = "the `{}` command can't be found".format(CMD_WDIFF)
    raise WdiffNotFoundError(msg)


def generate_wdiff(org_file, new_file, fold_breaks=False):
  """
  Returns the results from the `wdiff` command as a string.

  HTML `<ins>` and `<del>` tags will be used instead of the default markings.

  If *fold_breaks* is set, `<ins>` and `<del>` tags are allowed to span
  linesbreaks (option `-n` is not used).

  Raises:

    subrocess.CalledProcessError: on any `wdiff` process errors

  """
  check_for_wdiff()
  cmd = [CMD_WDIFF]
  cmd.extend(OPTIONS_OUTPUT)
  if not fold_breaks:
    cmd.extend(OPTIONS_LINEBREAK)
  cmd.extend([org_file, new_file])
  proc = sub.Popen(cmd, stdout=sub.PIPE)
  diff, _ = proc.communicate()
  return diff.decode('utf-8')


def build_paragraph(content, fold_breaks=False):
  """
  Returns *content* wrapped in `<p>` tags.

  All linebreaks (`\\n`) except the last are prepended with `<br />` tags,
  unless *fold_breaks* is set.

  """
  lines = list(filter(None, [line.strip() for line in content.split('\n')]))
  if not fold_breaks:
    for line_number in range(len(lines) - 1):
      lines[line_number] = "{}<br />".format(lines[line_number])
  return "<p>{}</p>".format('\n'.join(lines))


def wrap_paragraphs(content, fold_breaks=False):
  """
  Returns *content* with all paragraphs wrapped in `<p>` tags.

  If *fold_breaks* is set, linebreaks are not replaced with `<br />` tags.

  """
  paras = filter(None, [para.strip() for para in content.split('\n\n')])
  paras = [build_paragraph(para, fold_breaks) for para in paras]
  return '\n'.join(paras)


def wrap_content(org_file, new_file, content, fold_breaks=False):
  """
  Returns *content* wrapped in a HTML structure.

  If *fold_breaks* is set, linebreaks are not replaced with `<br />` tags.

  """
  paras = wrap_paragraphs(content, fold_breaks)
  context = {
    'org_file': Path(org_file).name,
    'new_file': Path(new_file).name,
    'content': paras,
    'css': CSS,
    'js': JS,
  }
  return TEMPLATE.format(**context)

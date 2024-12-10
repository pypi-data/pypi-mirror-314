from contextlib import nullcontext
from importlib import resources
import logging
import os
from pathlib import Path
from shutil import copy2
import sys
import types
import zipfile
from typing import List
from io import BytesIO
import tempfile

from venv import EnvBuilder, CORE_VENV_DEPS

TK_FILES = ["tcl86t.dll", "tk86t.dll", "zlib1.dll", "_tkinter.pyd", "tcl", "tkinter"]
_PYTHON_VERSION = "3.12.8"
logger = logging.getLogger(__name__)


class EVenvBuilder(EnvBuilder):
    def __init__(self, options):
        self.with_tk = options.with_tk
        super().__init__(
            system_site_packages=options.system_site,
            clear=options.clear,
            symlinks=options.symlinks,
            upgrade=options.upgrade,
            with_pip=options.with_pip,
            prompt=options.prompt,
            upgrade_deps=options.upgrade_deps,
        )

    def create(self, env_dir: str):
        super().create(env_dir)
        env_dir = os.path.abspath(env_dir)
        if self.upgrade:
            return
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            with find_embeddable_zip() as bundle_zip_path:
                tmp_zip_path = tmpdir_path / bundle_zip_path.name
                copy2(bundle_zip_path, tmp_zip_path)
            if not self.with_tk:
                zin = zipfile.ZipFile(tmp_zip_path, "r")
                zout_io = BytesIO()
                zout = zipfile.ZipFile(zout_io, "w")
                remove_tk(zin, zout, delete_files=TK_FILES)
                zin.close()
                zout.close()
                with open(tmp_zip_path, 'wb') as f:
                    f.write(zout_io.getvalue())
            extract_zip(tmp_zip_path, env_dir)
            self.change_config(env_dir)

    def change_config(self, env_dir: str):
        context = types.SimpleNamespace()
        context.env_dir = env_dir
        context.env_name = os.path.split(env_dir)[1]
        context.prompt = self.prompt if self.prompt is not None else context.env_name
        executable = os.path.join(env_dir, "python.exe")
        context.executable = executable
        context.python_dir = env_dir

        context.cfg_path = path = os.path.join(context.env_dir, "pyvenv.cfg")
        with open(path, "w", encoding="utf-8") as f:
            f.write("home = %s\n" % context.python_dir)
            if self.system_site_packages:
                incl = "true"
            else:
                incl = "false"
            f.write("include-system-site-packages = %s\n" % incl)
            f.write("version = %d.%d.%d\n" % sys.version_info[:3])
            if self.prompt is not None:
                f.write(f"prompt = {context.prompt!r}\n")
            f.write("executable = %s\n" % os.path.realpath(context.executable))
            args = []
            nt = os.name == "nt"
            if nt and self.symlinks:
                args.append("--symlinks")
            if not nt and not self.symlinks:
                args.append("--copies")
            if not self.with_pip:
                args.append("--without-pip")
            if not self.with_tk:
                args.append("--without-tk")
            if self.system_site_packages:
                args.append("--system-site-packages")
            if self.clear:
                args.append("--clear")
            if self.upgrade:
                args.append("--upgrade")
            if self.upgrade_deps:
                args.append("--upgrade-deps")
            if self.orig_prompt is not None:
                args.append(f'--prompt="{self.orig_prompt}"')

            args.append(context.env_dir)
            args = " ".join(args)
            f.write(f"command = {sys.executable} -m evenv {args}\n")


def extract_zip(zip_path: Path, extract_to: str):
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_to)


def find_embeddable_zip():
    return resources.as_file(
        resources.files('evenv')
        / 'bundled'
        / f'python-{_PYTHON_VERSION}-embedtk-amd64.zip'
    )


def remove_tk(zin: zipfile.ZipFile, zout: zipfile.ZipFile, delete_files: List[str]):
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if item.filename[-4:].endswith(".zip"):
            with BytesIO(buffer) as nested_io:
                with zipfile.ZipFile(nested_io, "r") as nested_zin:
                    with BytesIO() as nested_out_io:
                        with zipfile.ZipFile(nested_out_io, "w") as nested_zout:
                            remove_tk(nested_zin, nested_zout, delete_files)
                        zout.writestr(item.filename, nested_out_io.getvalue())
                        continue

        to_delete = (item.filename in delete_files) or any(
            item.filename.startswith(delete_item) for delete_item in delete_files
        )
        if not to_delete:
            zout.writestr(item, buffer)


def main(args=None):
    import argparse

    parser = argparse.ArgumentParser(
        description="Creates virtual embeddable Python "
        "environments in one or "
        "more target "
        "directories.",
        epilog="Once an environment has been "
        "created, you may wish to "
        "activate it, e.g. by "
        "sourcing an activate script "
        "in its bin directory.",
    )
    parser.add_argument(
        "dirs",
        metavar="ENV_DIR",
        nargs="+",
        help="A directory to create the environment in.",
    )
    parser.add_argument(
        "--system-site-packages",
        default=True,
        action="store_true",
        dest="system_site",
        help="Give the virtual environment access to the " "system site-packages dir.",
    )

    if os.name == "nt":
        use_symlinks = False
    else:
        use_symlinks = True

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--symlinks",
        default=use_symlinks,
        action="store_true",
        dest="symlinks",
        help="Try to use symlinks rather than copies, "
        "when symlinks are not the default for "
        "the platform.",
    )
    group.add_argument(
        "--copies",
        default=not use_symlinks,
        action="store_false",
        dest="symlinks",
        help="Try to use copies rather than symlinks, "
        "even when symlinks are the default for "
        "the platform.",
    )
    parser.add_argument(
        "--clear",
        default=False,
        action="store_true",
        dest="clear",
        help="Delete the contents of the "
        "environment directory if it "
        "already exists, before "
        "environment creation.",
    )
    parser.add_argument(
        "--upgrade",
        default=False,
        action="store_true",
        dest="upgrade",
        help="Upgrade the environment "
        "directory to use this version "
        "of Python, assuming Python "
        "has been upgraded in-place.",
    )
    parser.add_argument(
        "--without-pip",
        dest="with_pip",
        default=True,
        action="store_false",
        help="Skips installing or upgrading pip in the "
        "virtual environment (pip is bootstrapped "
        "by default)",
    )
    parser.add_argument(
        "--without-tk",
        dest="with_tk",
        default=True,
        action="store_false",
        help="Skips installing tk in the "
        "virtual environment (tk is bootstrapped "
        "by default)",
    )
    parser.add_argument(
        "--prompt",
        help="Provides an alternative prompt prefix for " "this environment.",
    )
    parser.add_argument(
        "--upgrade-deps",
        default=False,
        action="store_true",
        dest="upgrade_deps",
        help=f'Upgrade core dependencies ({", ".join(CORE_VENV_DEPS)}) '
        "to the latest version in PyPI",
    )
    parser.add_argument(
        "--without-scm-ignore-files",
        dest="scm_ignore_files",
        action="store_const",
        const=frozenset(),
        default=frozenset(["git"]),
        help="Skips adding SCM ignore files to the environment "
        "directory (Git is supported by default).",
    )
    options = parser.parse_args(args)
    if options.upgrade and options.clear:
        raise ValueError("you cannot supply --upgrade and --clear together.")
    builder = EVenvBuilder(options)
    for d in options.dirs:
        builder.create(d)


if __name__ == "__main__":
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print("Error:", e, file=sys.stderr)

    sys.exit(rc)

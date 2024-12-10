"""
Manipulate passwords stored and encrypted using `pass`, the "standard UNIX password manager", based on GPG.

See: https://www.passwordstore.org/
"""
from contextlib import contextmanager
from datetime import datetime
from getpass import getpass
import logging
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory, mkstemp
from argparse import ArgumentParser
from pathlib import Path
from configparser import _UNSET
from zut import add_command, SimpleError
from uuid import uuid4

_logger = logging.getLogger(__name__)

_pass_dir = Path.home().joinpath('.password-store')
_gpg_id: str = _UNSET

def _add_arguments(parser: ArgumentParser):
    subparsers = parser.add_subparsers(title='subcommands')
    add_command(subparsers, _handle_list, name='ls')
    add_command(subparsers, _handle_show, name='show')
    add_command(subparsers, _handle_insert, name='insert')
    add_command(subparsers, remove_pass, name='rm')

def _handle():
    _handle_list()

_handle.add_arguments = _add_arguments


def _handle_list():
    """
    List password names.
    """
    gpg_id = get_pass_gpg_id()
    _logger.debug("GPG id: %s", gpg_id)
    for p in get_pass_list():
        print(p)


def _add_arguments(parser: ArgumentParser):
    parser.add_argument('name')

def _handle_show(name: str):
    """
    Show a password value.
    """
    try:
        password = get_pass(name)
        print(password)
        return 0
    except FileNotFoundError as err:
        _logger.error(err)
        return 2

_handle_show.add_arguments = _add_arguments


def _add_arguments(parser: ArgumentParser):
    parser.add_argument('name')
    parser.add_argument('password', nargs='?')

def _handle_insert(name: str, password: str|None = None):
    """
    Insert a new password.
    """
    if password is None:
        password = getpass("Password: ")
        confirm_password = None
        while confirm_password != password:
            if confirm_password is not None:
                _logger.error("Invalid password confirmation. Try again.")
            confirm_password = getpass("Confirm password: ")
    
    insert_pass(name, password)

_handle_insert.add_arguments = _add_arguments


def get_pass_list():
    passes: list[str] = []

    def recurse(dir: Path):
        for path in dir.iterdir():
            if path.is_dir():
                recurse(path)
            elif path.suffix == '.gpg' and not path.name.startswith('.'):
                path = path.relative_to(_pass_dir)
                passes.append(path.with_suffix('').as_posix())

    recurse(_pass_dir)
    passes.sort()
    return passes


def get_pass(name: str, fallback: str = _UNSET):
    path = get_pass_path(name)
    if not path.exists():
        if fallback is _UNSET:
            raise FileNotFoundError(f"Pass not found: {name}")
        else:
            _logger.debug("Pass not found: %s at %s", name, path)
            return None

    _logger.debug("Decrypt pass %s at %s", name, path)
    cp = subprocess.run(['gpg', '--batch', '--decrypt', path], capture_output=True)
    if cp.returncode != 0:
        if value := _decode_output_unknown_encoding(cp.stderr, strip=True):
            _logger.error(f"[gpg:{cp.returncode} stderr] {value}")
        if value := _decode_output_unknown_encoding(cp.stdout, strip=True):
            _logger.error(f"[gpg:{cp.returncode} stdout] {value}")
        raise ValueError(f"gpg --decrypt returned code {cp.returncode}")
    
    return cp.stdout.decode('utf-8')


def insert_pass(name: str, password: str):
    path = get_pass_path(name)
    gpg_id = get_pass_gpg_id()
    if not gpg_id:
        raise ValueError(f"Pass GPG id not registered")
    
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_in_fd = None
    tmp_in = None
    tmp_out = path.with_name(f'{path.name}.tmp')
    try:
        tmp_in_fd, tmp_in = mkstemp()
        with open(tmp_in, 'w', encoding='utf-8') as fp:
            fp.write(password)
        os.close(tmp_in_fd)
        tmp_in_fd = None
        
        _logger.debug("Encrypt pass %s at %s", name, path)
        cp = subprocess.run(['gpg', '--batch', '--output', tmp_out, '--encrypt', '--recipient', gpg_id, tmp_in], text=True, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            if value := _decode_output_unknown_encoding(cp.stderr, strip=True):
                _logger.error(f"[gpg:{cp.returncode} stderr] {value}")
            if value := _decode_output_unknown_encoding(cp.stdout, strip=True):
                _logger.error(f"[gpg:{cp.returncode} stdout] {value}")
            raise SimpleError(f"gpg --encrypt returned code {cp.returncode}")
        if path.exists():
            archive_path = path.with_name(f".{path.stem}-{datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y%m%d-%H%M%S')}.gpg")
            oc = 2
            while archive_path.exists():
                archive_path = archive_path.with_name(f"{archive_path.stem}-{oc}.gpg")
                oc += 1
            path.rename(archive_path)
        tmp_out.rename(path)
    finally:
        if tmp_in_fd:
            os.close(tmp_in_fd)
        if tmp_in and os.path.exists(tmp_in):
           os.unlink(tmp_in)
        if tmp_out.exists():
            tmp_out.unlink()


def _add_arguments(parser: ArgumentParser):
    parser.add_argument('name')

def remove_pass(name: str):
    """
    Remove a password.
    """
    path = get_pass_path(name)
    if not path.exists():
        _logger.error(f"Pass does not exist: {name}")
        return False
    path.unlink()
    return True

remove_pass.add_arguments = _add_arguments


def get_pass_gpg_id():
    global _gpg_id
    if _gpg_id is _UNSET:
        path = _pass_dir.joinpath('.gpg-id')
        if path.exists():
            _gpg_id = path.read_text('utf-8').strip()
        else:
            _gpg_id = None        
    return _gpg_id


def get_pass_path(name: str):
    if not name:
        raise ValueError(f"Name cannot be empty")
    name = re.sub(r'\\', '', name)
    parts = name.split('/')
    path = _pass_dir.joinpath(*parts)
    return path.with_name(f'{path.name}.gpg')


def _decode_output_unknown_encoding(output: bytes, strip=False):
    if output is None:
        return None
    try:
        value = output.decode('utf-8')
    except UnicodeDecodeError:
        value = output.decode('cp1252')

    if strip:
        value = value.strip()
    return value


@contextmanager
def open_pass(file: Path|str, password_name: str, buffering: int = -1, encoding: str = None, newline: str = None, **kwargs):
    """
    Open a file encrypted using `pass` with the given password name.
    """
    password = get_pass(password_name)

    tmpdir = TemporaryDirectory()
    fp = None
    try:
        tmp = os.path.join(tmpdir.name, str(uuid4()))

        _logger.debug("Decrypt %s to %s using %s", file, tmp, password_name)
        cp = subprocess.run(['gpg', '--batch', '--output', tmp, '--passphrase-fd', '0', '--decrypt', file], text=True, stdout=sys.stdout, stderr=sys.stderr, input=password)
        if cp.returncode != 0:
            if value := _decode_output_unknown_encoding(cp.stderr, strip=True):
                _logger.error(f"[gpg:{cp.returncode} stderr] {value}")
            if value := _decode_output_unknown_encoding(cp.stdout, strip=True):
                _logger.error(f"[gpg:{cp.returncode} stdout] {value}")
            raise SimpleError(f"gpg --encrypt returned code {cp.returncode}")
        
        fp = open(tmp, 'r', buffering=buffering, encoding=encoding, newline=newline, **kwargs)
        yield fp

    finally:
        if fp:
            fp.close()
        tmpdir.cleanup()

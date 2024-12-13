#
#  Copyright (c) 2018-2024 Renesas Inc.
#  Copyright (c) 2018-2024 EPAM Systems Inc.
#
# pylint: disable=too-many-statements
import argparse
import logging
import os
import sys
import typing
from pathlib import Path

from aos_prov.actions import (
    add_node_to_unit,
    create_new_unit,
    download_image,
    provision_unit,
    remove_node_from_unit,
    remove_vm_unit,
    start_vm_unit,
)
from aos_prov.communication.cloud.cloud_api import DEFAULT_REGISTER_PORT, CloudAPI
from aos_prov.utils import DEFAULT_USER_CERT_PATH, DEFAULT_USER_KEY_PATH
from aos_prov.utils.common import AOS_DISKS_PATH, DISK_IMAGE_DOWNLOAD_URL, print_error
from aos_prov.utils.errors import (
    CloudAccessError,
    DeviceRegisterError,
    OnUnitError,
    UnitError,
)
from aos_prov.utils.user_credentials import UserCredentials

try:
    from importlib.metadata import version  # noqa: WPS433
except ImportError:
    import importlib_metadata as version  # noqa: WPS433,WPS432,WPS440

_ARGUMENT_USER_CERTIFICATE = '--cert'
_ARGUMENT_USER_KEY = '--key'
_ARGUMENT_USER_PKCS12 = '--pkcs12'

_COMMAND_NEW_VM = 'vm-new'
_COMMAND_REMOVE_VM = 'vm-remove'
_COMMAND_START_VM = 'vm-start'
_COMMAND_UNIT_CREATE = 'unit-new'
_COMMAND_UNIT_NODE_ADD = 'unit-node-add'
_COMMAND_UNIT_NODE_REMOVE = 'unit-node-remove'
_COMMAND_DOWNLOAD = 'download'

_DEFAULT_USER_CERTIFICATE = str(Path.home() / '.aos' / 'security' / 'aos-user-oem.p12')

_MAX_PORT = 65535

os.environ['GRPC_VERBOSITY'] = 'ERROR'

logger = logging.getLogger(__name__)


def sanitize_path_to_file(path: typing.Union[str, None]) -> typing.Union[str, None]:
    if path is None:
        return None
    # According to the requirement, aos-prov should allow any real path to be used
    absolute_path = os.path.abspath(path)
    if not os.path.isfile(absolute_path):
        raise CloudAccessError(f'Path: {path} is not a file or does not exist.')
    return absolute_path


def sanitize_path_to_dir(path: typing.Union[str, None]) -> typing.Union[str, None]:
    if path is None:
        return None
    # According to the requirement, aos-prov should allow any real path to be used
    absolute_path = os.path.abspath(path)
    if not os.path.isdir(absolute_path):
        raise CloudAccessError(f'Path: {path} is not a directory or does not exist.')
    return absolute_path


def sanitize_port(port: typing.Union[int, None]) -> typing.Union[int, None]:
    if not isinstance(port, int) or port < 1 or port > _MAX_PORT:
        raise CloudAccessError(f'Port is not valid: {port}. Should be in range 1..{_MAX_PORT}')
    return port


def str2bool(arg_value):
    if isinstance(arg_value, bool):
        return arg_value
    if arg_value.lower() in {'yes', 'true'}:
        return True
    if arg_value.lower() in {'no', 'false'}:
        return False

    raise argparse.ArgumentTypeError('Boolean value expected.')


def _parse_args():  # noqa: WPS213
    parser = argparse.ArgumentParser(
        prog='aos-prov',
        description='The unit provisioning tool using gRPC protocol',
        epilog="Run 'aos-prov [COMMAND] --help' for more information about commands",
    )

    parser.add_argument(
        '-u',
        '--unit',
        required=False,
        help='Unit address in format IP_ADDRESS or IP_ADDRESS:PORT',
    )

    parser.add_argument(
        _ARGUMENT_USER_CERTIFICATE,
        default=DEFAULT_USER_CERT_PATH,
        help=f'User certificate file. Default = {DEFAULT_USER_CERT_PATH}',
    )

    parser.add_argument(
        _ARGUMENT_USER_KEY,
        default=DEFAULT_USER_KEY_PATH,
        help=f'User key file. Default = {DEFAULT_USER_KEY_PATH}',
    )

    parser.add_argument(
        '-p',
        _ARGUMENT_USER_PKCS12,
        required=False,
        help='Path to user certificate in pkcs12 format.',
        dest='pkcs',
        default=_DEFAULT_USER_CERTIFICATE,
    )

    parser.add_argument(
        '--register-port',
        default=DEFAULT_REGISTER_PORT,
        help=f'Cloud port. Default: {DEFAULT_REGISTER_PORT}',
        type=int,
    )

    parser.add_argument(
        '-w',
        '--wait-unit',
        action='store',
        metavar='N',
        help='Wait for unit to respond for the first time in seconds. Default = 0 means wait for 5 seconds',
        dest='wait_unit',
        default=0,
        type=int,
    )

    parser.set_defaults(which=None)

    parser.add_argument(
        '--nodes',
        required=False,
        type=int,
        help='Count of nodes for the VMs group Unit. Default = 2',
        default=2,
    )

    sub_parser = parser.add_subparsers(title='Commands')

    new_vm_command = sub_parser.add_parser(
        _COMMAND_NEW_VM,
        help='Create a new VMs group Unit',
    )
    new_vm_command.set_defaults(which=_COMMAND_NEW_VM)

    new_vm_command.add_argument(
        '-N',
        '--name',
        required=True,
        help='Name of the VMs group Unit',
    )

    new_vm_command.add_argument(
        '-D',
        '--disk',
        required=False,
        help='Full path to the AosCore-powered disk.',
        default=AOS_DISKS_PATH,
    )

    new_vm_command.add_argument(
        '--nodes',
        required=False,
        type=int,
        help='Count of nodes for the VMs group Unit. Default = 2',
        default=2,
    )

    remove_vm_command = sub_parser.add_parser(
        _COMMAND_REMOVE_VM,
        help='Remove the VMs group Unit',
    )
    remove_vm_command.set_defaults(which=_COMMAND_REMOVE_VM)

    remove_vm_command.add_argument(
        '-N',
        '--name',
        required=True,
        help='Name of the VMs group Unit',
    )

    start_vm_command = sub_parser.add_parser(
        _COMMAND_START_VM,
        help='Start the VMs group Unit',
    )
    start_vm_command.add_argument(
        '-N',
        '--name',
        required=True,
        help='Name of the VMs group Unit.',
    )

    start_vm_command.add_argument(
        '-H',
        '--headless',
        action='store_true',
        help='Start the VMs group Unit in headless mode.',
    )
    start_vm_command.set_defaults(which=_COMMAND_START_VM)

    create_unit_command = sub_parser.add_parser(
        _COMMAND_UNIT_CREATE,
        help='Create and provision a new VMs group Unit',
    )
    create_unit_command.set_defaults(which=_COMMAND_UNIT_CREATE)

    create_unit_command.add_argument(
        '-N',
        '--name',
        required=True,
        help='Name of the VMs group Unit',
    )

    create_unit_command.add_argument(
        '--disk',
        required=False,
        help='Full path to the AosCore-powered disk.',
        default=AOS_DISKS_PATH,
    )

    create_unit_command.add_argument(
        '--nodes',
        required=False,
        type=int,
        help='Count of nodes for the Unit. Default = 2',
        default=2,
    )

    create_unit_command.add_argument(
        '-H',
        '--headless',
        action='store_true',
        help='Start created VMs group Unit in headless mode.',
    )

    create_unit_command.add_argument(
        '-p',
        _ARGUMENT_USER_PKCS12,
        required=False,
        help='Path to user certificate in pkcs12 format',
        dest='pkcs',
        default=_DEFAULT_USER_CERTIFICATE,
    )

    add_unit_node_command = sub_parser.add_parser(
        _COMMAND_UNIT_NODE_ADD,
        help='Add dynamical node to the already presented VMs group Unit',
    )
    add_unit_node_command.set_defaults(which=_COMMAND_UNIT_NODE_ADD)

    add_unit_node_command.add_argument(
        '-N',
        '--name',
        required=True,
        help='Name of the VMs group Unit',
    )

    add_unit_node_command.add_argument(
        '--disk',
        required=True,
        help='Full path to the AosCore-powered dynamical disk.',
    )

    add_unit_node_command.add_argument(
        '-S',
        '--start',
        type=str2bool,
        nargs='?',
        const=True,
        default=True,
        help='Start Node of the VMs group Unit. Available options: [True, False, yes, no, true, false]. Default = True',
    )

    add_unit_node_command.add_argument(
        '-H',
        '--headless',
        action='store_true',
        help='Start Node of the VMs group Unit in headless mode.',
    )

    remove_unit_node_command = sub_parser.add_parser(
        _COMMAND_UNIT_NODE_REMOVE,
        help='Remove dynamical node from the already presented VMs group Unit.'
        ' Only "secondary-N" nodes can be removed.',
    )
    remove_unit_node_command.set_defaults(which=_COMMAND_UNIT_NODE_REMOVE)

    remove_unit_node_command.add_argument(
        '-N',
        '--name',
        required=True,
        help='Name of the VMs group Unit',
    )

    remove_unit_node_command.add_argument(
        '--node',
        required=True,
        help='Node of the VMs group Unit (starts with "secondary").',
    )

    remove_unit_node_command.add_argument(
        '-r',
        '--reboot',
        type=str2bool,
        nargs='?',
        const=True,
        default=True,
        help='Reboot all nodes into VM Group. Available options: [True, False, yes, no, true, false]. Default = True',
    )

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {version("aos-prov")}',  # noqa: WPS323,WPS237
    )

    download_command = sub_parser.add_parser(_COMMAND_DOWNLOAD, help='Download image')
    download_command.set_defaults(which=_COMMAND_DOWNLOAD)
    download_command.add_argument(
        '-a',
        '--address',
        dest='download_address',
        help='Address to download image',
    )

    download_command.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='Force overwrite existing file',
    )

    return parser.parse_args()


def create_and_sanitize_user_creds(args) -> UserCredentials:
    is_default_pkcs = args.pkcs == _DEFAULT_USER_CERTIFICATE
    if not is_default_pkcs and (args.cert != DEFAULT_USER_CERT_PATH or args.key != DEFAULT_USER_KEY_PATH):
        raise CloudAccessError('Only --pkcs12 or (--cert, --key) can be specified, but not both options.')
    cert: typing.Union[str, None] = None
    key: typing.Union[str, None] = None
    pkcs: typing.Union[str, None] = None
    if args.cert == DEFAULT_USER_CERT_PATH and args.key == DEFAULT_USER_KEY_PATH:
        pkcs = sanitize_path_to_file(args.pkcs)
    else:
        cert = sanitize_path_to_file(args.cert)
        key = sanitize_path_to_file(args.key)
    return UserCredentials(cert_file_path=cert, key_file_path=key, pkcs12=pkcs)


def main():
    status = 0
    args = _parse_args()

    try:  # noqa: WPS225
        if args.which is None:
            user_creds = create_and_sanitize_user_creds(args)
            register_port = sanitize_port(args.register_port)
            cloud_api = CloudAPI(user_creds, register_port)
            cloud_api.check_cloud_access()
            wait = args.wait_unit // 5 or 1
            provision_unit(args.unit, cloud_api, wait, nodes_count=args.nodes)

        if args.which == _COMMAND_DOWNLOAD:
            url = DISK_IMAGE_DOWNLOAD_URL
            if args.download_address:
                url = args.download_address
            download_image(url, args.force)

        if args.which == _COMMAND_NEW_VM:
            disk = sanitize_path_to_dir(args.disk)
            create_new_unit(args.name, None, disk, nodes_count=args.nodes)

        if args.which == _COMMAND_REMOVE_VM:
            remove_vm_unit(args.name)

        if args.which == _COMMAND_START_VM:
            start_vm_unit(args.name, args.headless)

        if args.which == _COMMAND_UNIT_CREATE:
            user_creds = create_and_sanitize_user_creds(args)
            disk = sanitize_path_to_dir(args.disk)
            create_new_unit(
                args.name,
                user_creds,
                disk,
                nodes_count=args.nodes,
                do_provision=True,
                headless=args.headless,
            )

        if args.which == _COMMAND_UNIT_NODE_ADD:
            disk = sanitize_path_to_file(args.disk)
            add_node_to_unit(args.name, disk, args.start, args.headless)

        if args.which == _COMMAND_UNIT_NODE_REMOVE:
            remove_node_from_unit(args.name, args.node, args.reboot)

    except CloudAccessError as exc:
        print_error(f'Failed during communication with the AosCloud with error: {exc}')
        status = 1
    except DeviceRegisterError as exc:
        print_error(f'FAILED with error: {exc}')
        status = 1
    except UnitError as exc:
        print_error(f'Failed during communication with device with error: \n {exc}')
        status = 1
    except OnUnitError as exc:
        print_error('Failed to execute the command!')
        print_error(f'Error: {exc} ')
        status = 1
    except (AssertionError, KeyboardInterrupt):
        print_error('Stopped by keyboard...')
        status = 1

    sys.exit(status)


if __name__ == '__main__':
    main()

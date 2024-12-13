#
#  Copyright (c) 2018-2024 Renesas Inc.
#  Copyright (c) 2018-2024 EPAM Systems Inc.
#
import os
import tempfile
from pathlib import Path
from typing import Optional

from aos_prov.utils import pem
from aos_prov.utils.errors import UserCredentialsError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives._serialization import (  # noqa: WPS436
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    load_key_and_certificates,
    load_pkcs12,
)
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID


def _extract_cloud_domain_from_cert(cert_bytes: bytes) -> str:
    """Get the Cloud domain name from user certificate.

    Args:
        cert_bytes: certificate content in bytes

    Returns:
        cloud domain from user certificate
    """
    _, certificate, _ = load_key_and_certificates(cert_bytes, None)
    return certificate.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value


def _pkcs12_to_pem(pkcs12_bytes: bytes):
    private_key, certificate, additional_certificates = load_key_and_certificates(
        pkcs12_bytes,
        ''.encode('utf8'),
        default_backend(),
    )

    cert_bytes = bytearray(certificate.public_bytes(Encoding.PEM))
    for add_cert in additional_certificates:  # noqa: WPS519
        cert_bytes += add_cert.public_bytes(Encoding.PEM)
    key_bytes = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    cert_bytes = bytes(cert_bytes)
    return cert_bytes, key_bytes


def _create_temp_file(data_write: bytes):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)  # pylint: disable=R1732
    tmp_file.write(data_write)
    tmp_file.close()
    return tmp_file.name


class TempCredentials:
    def __init__(
        self,
        certificate: Optional[bytes],
        key: Optional[bytes],
        cert_file_name: Optional[str],
        key_file_name: Optional[str],
    ):
        self._key_file_name = key_file_name
        self._cert_file_name = cert_file_name

        self._key = None
        self._certificate = None

        if certificate and key:
            self._key = key
            self._certificate = certificate

    def __enter__(self):  # noqa: D105
        if not self._key_file_name:
            self._key_file_name = _create_temp_file(self._key)
        if not self._cert_file_name:
            self._cert_file_name = _create_temp_file(self._certificate)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: D105
        if self._key:
            os.unlink(self._key_file_name)
            self._key_file_name = None
        if self._certificate:
            os.unlink(self._cert_file_name)
            self._cert_file_name = None

    @property
    def key_file_name(self):
        return self._key_file_name

    @property
    def cert_file_name(self):
        return self._cert_file_name


class UserCredentials:

    def __init__(self, cert_file_path: Optional[str], key_file_path: Optional[str], pkcs12: Optional[str]):
        self._cert_file_path = cert_file_path
        self._key_file_path = key_file_path
        self._cloud_url = None
        if pkcs12:
            if Path(pkcs12).exists():
                with open(pkcs12, 'rb') as pkcs12_file:
                    pkcs12_file_content = pkcs12_file.read()
                    cert_bytes, key_bytes = _pkcs12_to_pem(pkcs12_file_content)
                    self._user_credentials = TempCredentials(
                        certificate=cert_bytes, key=key_bytes, cert_file_name=None, key_file_name=None,
                    )
                    self._cloud_url = _extract_cloud_domain_from_cert(pkcs12_file_content)
            else:
                if not Path(cert_file_path).exists() or not Path(key_file_path).exists():
                    raise UserCredentialsError(f'User credentials file {pkcs12} not found.')

                self._user_credentials = TempCredentials(
                    cert_file_name=cert_file_path,
                    key_file_name=key_file_path,
                    certificate=None,
                    key=None,
                )
                self._cloud_url = self._extract_cloud_url()

        else:
            if not Path(cert_file_path).exists():
                raise UserCredentialsError(f'User credentials file {cert_file_path} not found.')
            if not Path(key_file_path).exists():
                raise UserCredentialsError(f'User credentials file {key_file_path} not found.')

            self._user_credentials = TempCredentials(
                cert_file_name=cert_file_path,
                key_file_name=key_file_path,
                certificate=None,
                key=None,
            )
            self._cloud_url = self._extract_cloud_url()

    @property
    def cloud_url(self):
        return self._cloud_url

    @property
    def user_credentials(self):
        return self._user_credentials

    def _extract_cloud_url(self):
        """Get the Cloud domain name from user certificate.

        Returns:
            Organization name (url) from certificate content
        """
        with open(self._cert_file_path, 'rb') as cert:
            cert_data = cert.read()
            try:
                certificate = load_pkcs12(cert_data, password=None).cert.certificate
            except Exception:
                certificate = self._parse_pem(cert_data)

            org_list = certificate.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
            if org_list:
                return org_list[0].value
            return 'aoscloud.io'

    def _parse_pem(self, input_data: bytes):
        if not input_data:
            return None

        obj_list = pem.parse(input_data)

        for inst in obj_list:
            if isinstance(inst, pem.Certificate):
                return load_pem_x509_certificate(data=inst.as_bytes())
        return None

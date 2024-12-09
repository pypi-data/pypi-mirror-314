#!/usr/bin/python3
# ruff: noqa: F811,SLF001,D103
import pathlib as pl

import pytest
from dotenv import dotenv_values
from armis import ArmisCloud
import httpx
import ssl
import sys


def test_ssl():
    envfile = pl.Path.home() / ".env"
    config = dotenv_values(envfile)
    if "TEST_ARMIS_TENANT_HOSTNAME" not in config:
        pytest.skip("missing TEST_ARMIS_TENANT_HOSTNAME from env file")

    if "TEST_ARMIS_API_SECRET_KEY" not in config:
        pytest.skip("missing TEST_ARMIS_API_SECRET_KEY from env file")

    a = ArmisCloud(
        api_secret_key=config["TEST_ARMIS_API_SECRET_KEY"],
        tenant_hostname=config["TEST_ARMIS_TENANT_HOSTNAME"],
        log_level="DEBUG",
        api_page_size=5_000,
    )

    # ssl_config = httpx._config.SSLConfig()
    # ssl_context = ssl_config.load_ssl_context()
    ssl_context = ssl.create_default_context()

    if sys.version_info >= (3, 10) or ssl.OPENSSL_VERSION_INFO >= (1, 1, 0, 7):
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
    else:
        ssl_context.options |= ssl.OP_NO_SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3
        # ssl_context.options |= ssl.OP_NO_TLSv1
        # ssl_context.options |= ssl.OP_NO_TLSv1_2
        ssl_context.options |= ssl.OP_NO_TLSv1_3

    c = httpx.Client(
        follow_redirects=True,
        http2=True,
        trust_env=False,
        verify=ssl_context,
    )

    print(c.get("https://training.armis.com/"))

    # print("ssl_context.options=", ssl_context.options)

    # x = a.get_sites()
    # print("x=", x)

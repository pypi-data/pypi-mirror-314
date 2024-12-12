# -*- coding: utf-8 -*-
"""Configuration options for Azure discovery migration."""
import ipaddress
import json
import pathlib
import typing as t

import yaml
import pydantic
from pydantic import constr  # Constrained string type.
from pydantic import Field, ValidationError, root_validator, validator
from naterminator.core.Globals import Globals
from naterminator.core.config_vpc_migration import DiscoveryConfiguration
from naterminator.core.ConfigAdaptorVpcMigration import ConfigAdaptorVpcMigration

if not hasattr(t, "Literal"):
    from typing_extensions import Literal

    t.Literal = Literal


CIDRList = t.List[ipaddress.IPv4Network]
IPAddressList = t.List[ipaddress.IPv4Address]
Tag = t.Dict[str, str]
Tags = t.List[Tag]
_str = constr(strip_whitespace=True)


def _default_network() -> CIDRList:
    return [ipaddress.IPv4Network("0.0.0.0/0")]

class _BaseModel(pydantic.BaseModel):
    discovery_only: t.ClassVar[bool] = False

    class Config:
        json_encoders = {
            ipaddress.IPv4Address: str,
            ipaddress.IPv4Network: str,
        }
        extra = "forbid"

class ModeIdConfig(pydantic.BaseModel):
    id: _str

    @validator("id")
    def validate_id(cls, v):
        if not v in Globals.ModeIds:
            raise ValueError(f"id must be one of {Globals.ModeIds}")
        return v
    
class WorkflowAccountConfig(_BaseModel):
    role_name: _str
    aws_account_id: t.Optional[_str] = None
    region: t.Optional[_str] = None

class ControllerConfig(_BaseModel):
    controller_ip: ipaddress.IPv4Address
    controller_user: _str
    controller_password_env: _str
    aws_account_name: t.Optional[_str] = None
    ctrl_role_app: t.Optional[_str] = "aviatrix-role-app"
    ctrl_role_ec2: t.Optional[_str] = "aviatrix-role-ec2"
    gateway_role_app: t.Optional[_str] = None
    gateway_role_ec2: t.Optional[_str] = None

class TagConfig(_BaseModel):
    key: _str
    value: _str

class TestConfig(_BaseModel):
    input_test_config: t.Optional[_str] = "test.config"
    output_test_config: t.Optional[_str] = "config.json"
    enable_test: t.Optional[bool] = False

class VpcConfig(_BaseModel):
    vpc_id: _str
    aws_account_id: _str
    role_name: _str
    spoke_gw_name: _str
    spoke_gw_size: t.Optional[_str] = None
    region: _str
    tag_route_table: t.Optional[TagConfig] = None
    eips: t.Optional[IPAddressList] = []

class BackupConfig(_BaseModel):
    backup_folder: t.Optional[_str] = "./backups"
    workflow_account: WorkflowAccountConfig = None
    s3_bucket: _str
    natgw_backup_dir: t.Optional[_str] = "natgw_backups"

class ReplaceNatGwWithNewEipConfig(ModeIdConfig):
    hs_mode: t.Optional[int] = 2
    controller: ControllerConfig
    test: TestConfig = Field(default_factory=TestConfig)
    vpc: VpcConfig
    horizontal_scaling: t.Optional[_str] = 2
    backup: BackupConfig
    log_output_path: t.Optional[_str] = "./"


def load_from_dict(config_dict: t.Dict):
    """Load natgw migration settings from a python dictionary.

    Args:
        config_dict: Python dictionary in which to load configuration
            settings from.

    Returns:
        Parsed natgw migration settings.
    """

    try:
        config = None
        mode = ModeIdConfig(**config_dict)
        if mode.id in Globals.ModeIds:
            if mode.id in Globals.VPC_MIGRATION_ModeIds:
                config = DiscoveryConfiguration(**config_dict)
            else:
                config = ReplaceNatGwWithNewEipConfig(**config_dict)
    except ValidationError as e:
        print(e.json())
        raise SystemExit(1) from e
    if config != None:
        config = dump_to_dict(config)
    return config


def dump_to_dict(config) -> t.Dict:
    """Dump natgw migration settings to a python dictionary.

    Args:
        config: natgw migration settings.

    Returns:
        Configuration dictionary.
    """
    json_data = config.json()
    data = json.loads(json_data)

    return data


def load_from_yaml(yml_path: pathlib.Path, discovery_only: bool = False):
    """Load natgw migration settings from a yaml.

    Args:
        yml_path: Path to location of natgw migration yaml.

    Returns:
        Parsed natgw migration settings.
    """
    with open(yml_path, "r") as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)
    
    return load_from_dict(data)



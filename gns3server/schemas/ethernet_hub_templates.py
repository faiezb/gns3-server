#
# Copyright (C) 2020 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from .templates import Category, TemplateBase
from .ethernet_hub_nodes import EthernetHubPort

from pydantic import Field
from typing import Optional, List


DEFAULT_PORTS = [
    dict(port_number=0, name="Ethernet0"),
    dict(port_number=1, name="Ethernet1"),
    dict(port_number=2, name="Ethernet2"),
    dict(port_number=3, name="Ethernet3"),
    dict(port_number=4, name="Ethernet4"),
    dict(port_number=5, name="Ethernet5"),
    dict(port_number=6, name="Ethernet6"),
    dict(port_number=7, name="Ethernet7"),
]


class EthernetHubTemplate(TemplateBase):

    category: Optional[Category] = "switch"
    default_name_format: Optional[str] = "Hub{0}"
    symbol: Optional[str] = ":/symbols/hub.svg"
    ports_mapping: Optional[List[EthernetHubPort]] = Field(DEFAULT_PORTS, description="Ports")

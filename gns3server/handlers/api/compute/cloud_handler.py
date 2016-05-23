# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 GNS3 Technologies Inc.
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

from gns3server.web.route import Route
from gns3server.schemas.nio import NIO_SCHEMA
from gns3server.compute.builtin import Builtin

from gns3server.schemas.cloud import (
    CLOUD_CREATE_SCHEMA,
    CLOUD_OBJECT_SCHEMA,
    CLOUD_UPDATE_SCHEMA
)


class CloudHandler:

    """
    API entry points for cloud
    """

    @Route.post(
        r"/projects/{project_id}/cloud/nodes",
        parameters={
            "project_id": "Project UUID"
        },
        status_codes={
            201: "Instance created",
            400: "Invalid request",
            409: "Conflict"
        },
        description="Create a new cloud instance",
        input=CLOUD_CREATE_SCHEMA,
        output=CLOUD_OBJECT_SCHEMA)
    def create(request, response):

        builtin_manager = Builtin.instance()
        node = yield from builtin_manager.create_node(request.json.pop("name"),
                                                      request.match_info["project_id"],
                                                      request.json.get("node_id"),
                                                      node_type="cloud")
        response.set_status(201)
        response.json(node)

    @Route.get(
        r"/projects/{project_id}/cloud/nodes/{node_id}",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            200: "Success",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Get a cloud instance",
        output=CLOUD_OBJECT_SCHEMA)
    def show(request, response):

        builtin_manager = Builtin.instance()
        node = builtin_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        response.json(node)

    @Route.put(
        r"/projects/{project_id}/cloud/nodes/{node_id}",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            200: "Instance updated",
            400: "Invalid request",
            404: "Instance doesn't exist",
            409: "Conflict"
        },
        description="Update a cloud instance",
        input=CLOUD_UPDATE_SCHEMA,
        output=CLOUD_OBJECT_SCHEMA)
    def update(request, response):

        builtin_manager = Builtin.instance()
        node = builtin_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        node.updated()
        response.json(node)

    @Route.delete(
        r"/projects/{project_id}/cloud/nodes/{node_id}",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance deleted",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Delete a cloud instance")
    def delete(request, response):

        builtin_manager = Builtin.instance()
        yield from builtin_manager.delete_node(request.match_info["node_id"])
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/cloud/nodes/{node_id}/start",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance started",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Start a cloud")
    def start(request, response):

        Builtin.instance().get_device(request.match_info["node_id"], project_id=request.match_info["project_id"])
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/cloud/nodes/{node_id}/stop",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance stopped",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Stop a cloud")
    def stop(request, response):

        Builtin.instance().get_device(request.match_info["node_id"], project_id=request.match_info["project_id"])
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/cloud/nodes/{node_id}/suspend",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance suspended",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Suspend a cloud")
    def suspend(request, response):

        Builtin.instance().get_device(request.match_info["node_id"], project_id=request.match_info["project_id"])
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/cloud/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/nio",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter on the cloud (always 0)",
            "port_number": "Port on the cloud"
        },
        status_codes={
            201: "NIO created",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Add a NIO to a cloud instance",
        input=NIO_SCHEMA,
        output=NIO_SCHEMA)
    def create_nio(request, response):

        builtin_manager = Builtin.instance()
        node = builtin_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        nio = yield from builtin_manager.create_nio(node, request.json["nio"])
        port_number = int(request.match_info["port_number"])
        yield from node.add_nio(nio, port_number)
        response.set_status(201)
        response.json(nio)

    @Route.delete(
        r"/projects/{project_id}/cloud/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/nio",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter on the cloud (always 0)",
            "port_number": "Port on the cloud"
        },
        status_codes={
            204: "NIO deleted",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Remove a NIO from a cloud instance")
    def delete_nio(request, response):

        builtin_manager = Builtin.instance()
        node = builtin_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        port_number = int(request.match_info["port_number"])
        nio = yield from node.remove_nio(port_number)
        yield from nio.delete()
        response.set_status(204)

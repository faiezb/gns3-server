#!/usr/bin/env python
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

import os

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from gns3server.db.repositories.computes import ComputesRepository
from gns3server import schemas

from .models import Base
from gns3server.config import Config

import logging

log = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:

    db_path = os.path.join(Config.instance().config_dir, "gns3_controller.db")
    db_url = os.environ.get("GNS3_DATABASE_URI", f"sqlite+aiosqlite:///{db_path}")
    engine = create_async_engine(db_url, connect_args={"check_same_thread": False}, future=True)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            log.info(f"Successfully connected to database '{db_url}'")
        app.state._db_engine = engine
    except SQLAlchemyError as e:
        log.error(f"Error while connecting to database '{db_url}: {e}")


async def get_computes(app: FastAPI) -> List[dict]:

    computes = []
    async with AsyncSession(app.state._db_engine) as db_session:
        db_computes = await ComputesRepository(db_session).get_computes()
        for db_compute in db_computes:
            try:
                compute = jsonable_encoder(
                    schemas.Compute.from_orm(db_compute), exclude_unset=True, exclude={"created_at", "updated_at"}
                )
            except ValidationError as e:
                log.error(f"Could not load compute '{db_compute.compute_id}' from database: {e}")
                continue
            computes.append(compute)
    return computes
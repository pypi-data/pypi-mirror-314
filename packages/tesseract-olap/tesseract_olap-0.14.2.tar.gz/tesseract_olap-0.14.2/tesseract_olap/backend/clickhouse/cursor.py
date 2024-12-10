import logging
import queue
from concurrent import futures
from typing import Dict, List

from clickhouse_driver.dbapi import Error as ClickhouseDbapiError
from clickhouse_driver.errors import Error as ClickhouseError

from tesseract_olap.exceptions.backend import BackendValidationError
from tesseract_olap.schema import CubeTraverser, SchemaTraverser

from .dialect import TypedCursor, TypedDictCursor
from .sqlbuild import membercountquery_sql

logger = logging.getLogger("tesseract_olap.backend.clickhouse")


def fetch_membercount(
    cursor_queue: "queue.Queue[TypedDictCursor]", cube: "CubeTraverser"
):
    """Threaded function to request member count for all levels in cube."""
    cursor = cursor_queue.get()

    try:
        query, meta = membercountquery_sql(cube)

        cursor.reset_cursor()
        for table in meta.tables:
            cursor.set_inline_table(table)
        cursor.execute(query.get_sql())

        result: Dict[str, int] = cursor.fetchone() or {"_empty": 0}
        return cube.name, result

    finally:
        cursor_queue.put(cursor)


def inyect_members_count(schema: "SchemaTraverser", cursor_list: List[TypedDictCursor]):
    """Updates the `count` property on all Levels in the Schema with the number of members, as returned by the provided cursors from the ClickhouseBackend.

    The process runs in parallel using as many cursors are passed as argument.
    """
    count_total = sum(
        len(hie.level_map)
        for cube in schema.cube_map.values()
        for dim in cube.dimensions
        for hie in dim.hierarchies
    )
    executor = futures.ThreadPoolExecutor(max_workers=len(cursor_list))

    cursor_queue = queue.Queue(maxsize=len(cursor_list))
    for cursor in cursor_list:
        cursor_queue.put(cursor)

    try:
        # Run queries in parallel
        promises = tuple(
            executor.submit(fetch_membercount, cursor_queue, cube)
            for cube in sorted(schema.cube_map.values(), key=lambda cube: cube.name)
        )

        # Wait for the results and process them
        count_progress = 0
        for future in futures.as_completed(promises, timeout=6 * len(promises)):
            try:
                result = future.result()
            except (ClickhouseDbapiError, ClickhouseError) as exc:
                logger.debug("Error retrieving count of members: %s", exc)
                continue

            cube_name, members = result

            count_progress += len(members)
            logger.debug(
                "[%d of %d] %r : %r", count_progress, count_total, cube_name, members
            )

            cube = schema.get_cube(cube_name)
            for level in cube.levels:
                count = members.get(level.name, 0)
                if count == 0:
                    logger.warning(
                        "Level(cube=%r, name=%r) returned 0 members",
                        cube.name,
                        level.name,
                    )
                level.count = count

    except KeyboardInterrupt:
        logger.debug("Interrupted by the user")

    finally:
        # Ensure children threads are terminated
        executor.shutdown(wait=False)


def validate_schema_tables(schema: "SchemaTraverser", cursor: "TypedCursor"):
    """Validates the declared set of table, columns in the Schema entities with the ones available in the Backend."""
    schema_tables = schema.unwrap_tables()
    logger.debug("Tables to validate: %d", len(schema_tables))

    cursor.execute(
        "SELECT table, groupArray(name) AS columns FROM system.columns WHERE table IN splitByChar(',', %(tables)s) GROUP BY table",
        {"tables": ",".join(schema_tables.keys())},
    )
    observed_tables = {
        table: set(columns) for table, columns in (cursor.fetchall() or [])
    }

    if schema_tables != observed_tables:
        reasons = []

        for table, columns in schema_tables.items():
            if table not in observed_tables:
                reasons.append(
                    f"- Table '{table}' is defined in Schema but not available in Backend"
                )
                continue

            difference = columns.difference(observed_tables[table])
            if difference:
                reasons.append(
                    f"- Schema references columns {difference} in table '{table}', but not available in Backend"
                )

        if reasons:
            message = (
                "Mismatch between columns defined in the Schema and available in ClickhouseBackend:\n%s"
                % "\n".join(reasons)
            )
            raise BackendValidationError(message)

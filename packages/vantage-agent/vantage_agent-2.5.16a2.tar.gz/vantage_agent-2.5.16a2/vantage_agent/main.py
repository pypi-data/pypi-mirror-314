"""Main module of the project for starting the agent."""

import asyncio

from loguru import logger

from vantage_agent.scheduler import init_scheduler, shut_down_scheduler
from vantage_agent.sentry import init_sentry


def sub_main():
    """Start the agent by initiating the scheduler."""
    logger.info("Starting the Vantage Agent")
    init_sentry()
    scheduler = init_scheduler()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):  # pragma: no cover
        logger.info("Shutting down the Vantage Agent")
        shut_down_scheduler(scheduler)  # pragma: no cover


def main():
    """Start the main program guaranteed to run in the main thread."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(sub_main())
    loop.close()

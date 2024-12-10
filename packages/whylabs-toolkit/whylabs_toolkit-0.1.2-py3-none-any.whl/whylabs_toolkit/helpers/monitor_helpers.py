import logging
from typing import Any, List, Optional

from whylabs_client.exceptions import ApiValueError
from whylabs_client.exceptions import NotFoundException, ForbiddenException

from whylabs_toolkit.helpers.config import Config
from whylabs_toolkit.helpers.utils import get_monitor_api, get_models_api
from whylabs_toolkit.utils.granularity import Granularity


BASE_ENDPOINT = "https://api.whylabsapp.com"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_monitor_config(org_id: str, dataset_id: str, config: Config = Config()) -> Any:
    api = get_monitor_api(config=config)
    try:
        monitor_config = api.get_monitor_config_v3(org_id=org_id, dataset_id=dataset_id)
        logger.info(f"Found monitor config for {dataset_id}")
        return monitor_config
    except NotFoundException:
        logger.info(f"Could not find a monitor config for {dataset_id}")
        return None
    except ForbiddenException as e:
        logger.warning(
            f"You don't have access to monitor config for {dataset_id}. Did you set a correct WHYLABS_API_KEY?"
        )
        raise e


def get_monitor(
    monitor_id: str, org_id: Optional[str] = None, dataset_id: Optional[str] = None, config: Config = Config()
) -> Any:
    org_id = org_id or config.get_default_org_id()
    dataset_id = dataset_id or config.get_default_dataset_id()

    api = get_monitor_api(config=config)
    try:
        monitor = api.get_monitor(org_id=org_id, dataset_id=dataset_id, monitor_id=monitor_id)
        return monitor
    except NotFoundException:
        logger.info(f"Didn't find a monitor with id {monitor_id} for {dataset_id}. Creating a new one...")
        return None
    except ForbiddenException as e:
        logger.warning(
            f"You don't have access to monitor {monitor_id} for {dataset_id}. Did you set a correct WHYLABS_API_KEY?"
        )
        raise e


def get_analyzer_ids(
    monitor_id: str, org_id: Optional[str] = None, dataset_id: Optional[str] = None, config: Config = Config()
) -> Any:
    org_id = org_id or config.get_default_org_id()
    dataset_id = dataset_id or config.get_default_dataset_id()
    try:
        monitor_config = get_monitor_config(org_id=org_id, dataset_id=dataset_id, config=config)

        if monitor_config:
            for item in monitor_config.get("monitors"):
                if item["id"] == monitor_id:
                    resp = item["analyzerIds"]
                    return resp

    except NotFoundException:
        logger.warning(f"Could not find analyzer IDs for {org_id}, {dataset_id}, {monitor_id}")
        return None

    except ForbiddenException:
        logger.error(f"Could not get analyzer id's due to a ForbiddenException, did you set a correct WHYLABS_API_KEY?")
        return None

    except Exception as e:
        raise e


def get_analyzers(
    monitor_id: str, org_id: Optional[str] = None, dataset_id: Optional[str] = None, config: Config = Config()
) -> Optional[List[Any]]:
    org_id = org_id or config.get_default_org_id()
    dataset_id = dataset_id or config.get_default_dataset_id()
    api = get_monitor_api(config=config)
    analyzers = []
    analyzer_ids = get_analyzer_ids(org_id=org_id, dataset_id=dataset_id, monitor_id=monitor_id, config=config)
    if analyzer_ids:
        for analyzer in analyzer_ids:
            analyzers.append(api.get_analyzer(org_id=org_id, dataset_id=dataset_id, analyzer_id=analyzer))
        return analyzers
    else:
        return None


def time_period_to_granularity(time_period: str) -> Granularity:
    if time_period == "PT1H":
        return Granularity.hourly

    if time_period == "P1W":
        return Granularity.weekly

    if time_period == "P1M":
        return Granularity.monthly

    return Granularity.daily


def get_model_granularity(
    org_id: Optional[str] = None, dataset_id: Optional[str] = None, config: Config = Config()
) -> Optional[Granularity]:
    org_id = org_id or config.get_default_org_id()
    dataset_id = dataset_id or config.get_default_dataset_id()

    api = get_models_api(config=config)
    model_meta = api.get_model(org_id=org_id, model_id=dataset_id)

    if model_meta:
        return time_period_to_granularity(model_meta["time_period"])
    return None


def delete_monitor(
    monitor_id: str, org_id: Optional[str] = None, dataset_id: Optional[str] = None, config: Config = Config()
) -> None:
    org_id = org_id or config.get_default_org_id()
    dataset_id = dataset_id or config.get_default_dataset_id()

    api = get_monitor_api(config=config)
    try:
        analyzer_ids = get_analyzer_ids(org_id=org_id, dataset_id=dataset_id, monitor_id=monitor_id, config=config)
        if analyzer_ids is None:
            return
        for analyzer_id in analyzer_ids:
            resp_analyzer = api.delete_analyzer(org_id=org_id, dataset_id=dataset_id, analyzer_id=analyzer_id)
            logger.debug(f"Deleted analyzer with Resp:{resp_analyzer}")
        resp_monitor = api.delete_monitor(org_id=org_id, dataset_id=dataset_id, monitor_id=monitor_id)
        logger.debug(f"Deleted monitor with Resp:{resp_monitor}")
    except ApiValueError as e:
        logger.error(f"Error deleting monitor {monitor_id}: {e.msg}")  # type: ignore
        raise e


def list_monitors(org_id: Optional[str], dataset_id: Optional[str], config: Config = Config()) -> List[str]:
    org_id = org_id or config.get_default_org_id()
    dataset_id = dataset_id or config.get_default_dataset_id()

    try:
        monitors = get_monitor_config(org_id=org_id, dataset_id=dataset_id)
        if monitors is not None:
            return [monitor["id"] for monitor in monitors.get("monitors")]
        else:
            logger.info(f"No monitors found for {dataset_id}")
            return []
    except ForbiddenException as e:
        logger.warning(
            f"You don't have access to monitor list for {dataset_id}. Did you set a correct WHYLABS_API_KEY?"
        )
        raise e
    except Exception as e:
        logger.error(f"Error listing monitors for {dataset_id}: {e}")
        raise e

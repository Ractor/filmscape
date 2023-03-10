import django
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from requests import JSONDecodeError

from filmscape import settings
from filmscape.utils import create_or_update_video_instances, delete_obsolete_video_instances

logger = get_task_logger(__name__)


@shared_task
def sync_films_from_external_api():
    """
    Downloads data from the external API, saves it into the database and removes the obsolete records.
    """
    # Request data from the API
    try:
        logger.info('Requesting data from the API.')
        r = requests.get(settings.FILMSCAPE_API_URL)
        logger.info('Decoding requested data.')
        data = r.json()
    except (JSONDecodeError, ConnectionError) as err:
        logger.error(f'Error occurred during API data processing: {err}')
        return False

    # Process returned data
    logger.info('Processing fetched data.')
    ok, instances = create_or_update_video_instances(data, logger)

    delete_obsolete_video_instances(instances, logger)
    logger.info(f'Processing ended {"successfully" if ok else "with errors"}.')

import json
import sys
import threading
import time
from lgt_common.pubsub.pubsubfactory import PubSubFactory
import logging as log
from lgt_jobs.env import project_id, background_jobs_topic, background_jobs_subscriber
from lgt_jobs.runner import BackgroundJobRunner
from lgt_jobs import jobs_map
import google.cloud.logging

lock = threading.Lock()


def run_background_job(data):
    try:
        log.info(f"[JOB]: {data} [START]")
        BackgroundJobRunner.run(jobs_map=jobs_map, data=data)
        log.info(f"[JOB]: {data} [FINISHED]")
    except Exception:
        raise


def run_background_job_with_lock(message):
    try:
        data = json.loads(message.data)
        with lock:
            run_background_job(data)
    except:
        import traceback
        log.error(f"[ERROR][JOB]: {message.data} [ERROR] {traceback.format_exception(*sys.exc_info())} ")
        traceback.print_exception(*sys.exc_info())
    finally:
        # accept message any way
        message.ack()


if __name__ == '__main__':
    client = google.cloud.logging.Client()
    client.setup_logging()
    factory = PubSubFactory(project_id)
    factory.create_topic_if_doesnt_exist(background_jobs_topic)
    factory.create_subscription_if_doesnt_exist(background_jobs_subscriber, background_jobs_topic, 600)
    bot_subscription_path = factory.get_subscription_path(background_jobs_subscriber, background_jobs_topic)
    factory.subscriber.subscribe(bot_subscription_path, callback=run_background_job_with_lock)
    while True:
        time.sleep(1)

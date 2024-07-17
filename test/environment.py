import logging
import os
import pdb

from playwright.sync_api import sync_playwright

VIDEO_DIR = 'videos/'
SCENARIO_COUNTER = 0


def before_all(context):
    for subdir in ['build', 'videos']:
        os.makedirs(subdir, exist_ok=True)
    python_log = logging.FileHandler(filename='build/python.log')
    python_log.setLevel(logging.INFO)
    python_log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(python_log)
    context.config.setup_logging()
    logging.info('============ started behave ====================================')

    context.playwright = sync_playwright().start()


def before_scenario(context, scenario):
    logging.info(f'{scenario.feature}.{scenario}')
    context.browser = context.playwright.chromium.launch(headless=False)
    context.browser_context = context.browser.new_context(record_video_dir=VIDEO_DIR)
    context.page = context.browser_context.new_page()


def after_scenario(context, scenario):
    global SCENARIO_COUNTER  # pylint: disable=global-statement

    try:
        SCENARIO_COUNTER += 1

    finally:
        context.page.close()
        context.browser_context.close()
        context.browser.close()

        video_path = context.page.video.path()
        video_path_new = f'{VIDEO_DIR}/{SCENARIO_COUNTER:05}__'
        video_path_new += scenario.status.name + '__'  # passed or failed
        video_path_new += scenario.filename.split('/')[-1] + '__'
        video_path_new += scenario.name.replace(' ', '_') + '.'
        video_path_new += video_path.split('.')[-1]
        os.rename(video_path, video_path_new)
        logging.info(f'saved {video_path}')


def after_step(context, step):
    allow_post_mortems(context, step)


def allow_post_mortems(context, step):
    '''
    Allow post-mortem debugging, if enabled via environment.
    This short illustrated answer explains how it works and why it is so good: https://stackoverflow.com/a/61690358/5140740
    '''
    if 'post_mortem' in os.environ and step.status == 'failed':
        # Similar to 'behave --no-capture' calling stop_capture() ensures visibility of pdb's prompts,
        # while still supporting capture until an uncaught error occurs (yes, relying on behave's internal function)
        context._runner.stop_capture()  # pylint: disable=protected-access
        pdb.post_mortem(step.exc_traceback)

import logging
import os
from pathlib import Path
from time import sleep

SCENARIO_COUNTER = 0


class Playwright:
    """Integrates Playwright with behave."""

    BUILD_DIR = 'build'
    VIDEO_DIR = 'videos'
    TRACE_DIR = os.path.join(VIDEO_DIR, 'traces')

    @classmethod
    def before_all(cls, context):
        for folder in [cls.BUILD_DIR, cls.TRACE_DIR]:
            os.makedirs(folder, exist_ok=True)

        cls.__setup_logging(context, os.path.join(cls.BUILD_DIR, 'python.log'))
        context.playwright = cls.__setup_playwright()

    @classmethod
    def before_scenario(cls, context, scenario):
        logging.info(f'{scenario.feature}.{scenario}')
        context.browser = context.playwright.chromium.launch(headless=False)
        context.browser_context = context.browser.new_context(record_video_dir=cls.VIDEO_DIR,
                                                              ignore_https_errors=True)
        context.browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
        context.page = context.browser_context.new_page()

        def iframe():
            return context.page.frame_locator('iframe')

        context.iframe = iframe

    @classmethod
    def before_step(cls, context, step_):
        def format_table(table):
            if not table:
                return ''

            # Determine the maximum width for each column
            widths = [max(len(str(cell)) for cell in col) for col in zip(*([table.headings] + list(table)))]

            # Create a formatted row with aligned columns
            def format_row(row):
                return '| ' + ' | '.join(f'{str(cell):<{width}}' for cell, width in zip(row, widths)) + ' |'

            # Format the header and rows
            header = format_row(table.headings)
            rows = '\n'.join(format_row(row) for row in table)

            return f'{header}\n{rows}'

        if 'OVERLAY' in os.environ:
            table = format_table(step_.table) if step_.table else ''
            message = f'{step_.keyword} {step_.name}\n{table or step_.text or ""}'
            seconds = os.environ['OVERLAY']
            if seconds:
                cls.overlay_message(context.page, message, int(seconds))
            else:
                cls.overlay_message(context.page, message)

    @classmethod
    def after_scenario(cls, context, scenario):
        trace_file = Path.cwd().absolute() / 'trace.zip'
        video_file = context.page.video.path()

        context.browser_context.tracing.stop(path=trace_file)
        context.page.close()
        context.browser_context.close()
        context.browser.close()
        cls.__rename_files(video_file, trace_file, scenario, cls.VIDEO_DIR, cls.TRACE_DIR)

    @staticmethod
    def after_step(context, step):
        allow_post_mortems(context, step)

    @classmethod
    def __setup_playwright(cls):
        """Get Playwright for use with behave. Call from before_all(context)."""
        # pylint: disable=import-error
        from playwright.sync_api import sync_playwright
        manager = sync_playwright()
        return type(manager).__enter__(manager)  # pylint: disable=unnecessary-dunder-call

    @staticmethod
    def overlay_message(page, message, seconds=1):
        """
        Show a message on a Playwright-controlled browser page, and remove it after the given number of seconds.

        Useful for self-explanatory videos, so anyone can understand a test without looking at logs or feature files.
        """
        # some feature files may contain literal \n like this, so we escape them, to show without any interpretation:
        # "de": "über Berliner Tor \n Hauptbahnhof Nord"
        message = message.replace('\\n', '\\\\n')

        page.evaluate(f"""
            const overlay = document.createElement('playwright-overlay');
            overlay.id = 'playwright-overlay';
            overlay.style.position = 'fixed';
            overlay.style.bottom = '50px';
            overlay.style.left = '10px';
            overlay.style.backgroundColor = 'rgba(202, 202, 202, 1)';
            overlay.style.color = 'rgba(25, 25, 25, 1)';
            overlay.style.padding = '10px';
            overlay.style.fontSize = '16px';
            overlay.style.borderRadius = '5px';
            overlay.style.zIndex = '10000';
            overlay.style.fontFamily = 'monospace';
            overlay.style.pointerEvents = 'none';
            overlay.style.mixBlendMode = 'normal';

            const pre = document.createElement('pre');
            pre.style.margin = '0'; // Reset margin for better spacing
            pre.innerText = `{message}`;
            overlay.appendChild(pre);

            document.body.appendChild(overlay);
        """)
        sleep(seconds)
        page.evaluate("""
            const overlay = document.getElementById('playwright-overlay');
            document.body.removeChild(overlay);
        """)

    @staticmethod
    def __setup_logging(context, filename):
        """Set up behave-compatible logging."""
        python_log = logging.FileHandler(filename)
        python_log.setLevel(logging.INFO)
        python_log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger('').addHandler(python_log)
        context.config.setup_logging()
        logging.info('============ started behave ====================================')

    @staticmethod
    def __rename_files(video_file, trace_file, scenario, video_dir, trace_dir):
        """
        Rename/move video/trace files to appear in Jenkins Build Artifacts according to run order, status and name.

        Example:
        00001__passed__end_to_end.feature__Make_a_notice_appear_on_a_display.webm
        00002__passed__end_to_end.feature__Make_an_incident_appear_on_a_display.webm
        00003__passed__end_to_end.feature__Playback_announcement.webm
        """
        def name_by_scenario(scenario):
            name = scenario.status.name + '__'  # passed or failed
            name += os.path.split(scenario.filename)[-1] + '__'
            name += scenario.name.replace(' ', '_') + '.'
            return name

        global SCENARIO_COUNTER  # pylint: disable=global-statement
        SCENARIO_COUNTER += 1
        video_file_new = os.path.join(video_dir, f'{SCENARIO_COUNTER:05}__')
        video_file_new += name_by_scenario(scenario)
        video_file_new += video_file.split('.')[-1]
        os.rename(video_file, video_file_new)
        logging.info(f'saved {video_file}')

        if scenario.status.name == 'passed':
            os.unlink(trace_file)
        else:
            trace_path_new = os.path.join(trace_dir, f'{SCENARIO_COUNTER:05}__')
            trace_path_new += name_by_scenario(scenario) + 'zip'
            os.rename(trace_file, trace_path_new)
            logging.info(f'saved {trace_path_new}')


def close_asyncio_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None
    if loop is not None:
        loop.close()


def allow_post_mortems(context, step):
    """
    Allow post-mortem debugging with behave.

    The power of post-mortem debugging: https://almarklein.org/pm-debugging.html
    To enable, call this function from after_step(context, step) and set the `post_mortem` flag in the environment.
    """
    import os
    if 'post_mortem' in os.environ and step.status == 'failed':
        # Similar to 'behave --no-capture' calling stop_capture() ensures visibility of pdb's prompts,
        # while still supporting capture until an uncaught error occurs (yes, relying on behave's internal function)
        # https://stackoverflow.com/a/61690358/5140740
        context._runner.stop_capture()  # pylint: disable=protected-access
        import pdb
        pdb.post_mortem(step.exc_traceback)

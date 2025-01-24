import logging
import os
import pdb

from playwright.sync_api import sync_playwright
from behave_playwright import Playwright

VIDEO_DIR = 'videos/'
SCENARIO_COUNTER = 0


def before_all(context):
    Playwright.before_all(context)


def before_scenario(context, scenario):
    Playwright.before_scenario(context, scenario)


def after_scenario(context, scenario):
    try:
        pass
    finally:
        Playwright.after_scenario(context, scenario)


def before_step(context, step):
    Playwright.before_step(context, step)


def after_step(context, step):
    Playwright.after_step(context, step)

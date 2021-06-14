import requests
from bs4 import BeautifulSoup
import os
import itertools
# import logging
from selenium import webdriver
import json
import time
import database
import re
from selenium.common.exceptions import *
import asyncio
import multiprocessing
import tkinter as tk
import tkinter.ttk as ttk
from itertools import zip_longest
from data_collector import parse
from database import DBConnection

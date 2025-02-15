from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.sync import TelegramClient 
from telethon.errors import (
    PeerFloodError, 
    UserPrivacyRestrictedError, 
    FloodWaitError, 
    UserNotMutualContactError,
    ChatAdminRequiredError, 
    InputUserDeactivatedError,
    UserKickedError, 
    ChannelPrivateError)
from telethon.sessions import StringSession
from telethon.network import ConnectionTcpAbridged

import sys
import csv
import traceback
import time
import random 
import configparser
import os
import uuid
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from time import sleep
from abc import ABC, abstractmethod
from random import randint
import traceback
import requests
from tkinter import filedialog, messagebox
import asyncio
import aiofiles
import io
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
import sys
import csv
import traceback
import time
import random
import configparser
import os
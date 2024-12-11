#    ___                         ____           _           ___            _         __       
#   / _ \___  __ _  ___ ____    / __/_ _  ___  (_)______   / _ \___ __ _  (_)__  ___/ /__ ____
#  / , _/ _ \/  ' \/ _ `/ _ \  / _//  ' \/ _ \/ / __/ -_) / , _/ -_)  ' \/ / _ \/ _  / -_) __/
# /_/|_|\___/_/_/_/\_,_/_//_/ /___/_/_/_/ .__/_/_/  \__/ /_/|_|\__/_/_/_/_/_//_/\_,_/\__/_/   
#                                      /_/                                                     
#
# Version: ?
# Last Updated: 7/8/2024
# Creator & Maintainer: Kendrick Fithen
# Contributor(s): John Reed

import datetime
import json
import os
from pathlib import Path
from pygame import mixer
import platform
import pyttsx3
import random
import time

from .notification import Notification, GetNotifier

class RomanEmpireReminder:
    def __init__(self, path: Path) -> None:
        # get the root for our data files (Audio, Config.json, Image, etc.)
        self.path = path

        self.NotificationIndex = 0
        self.NotificationArray = []

        with open(self.path / 'Config.json', 'r') as NotificationConfig:
            ConfigData = json.load(NotificationConfig)
            self.NotificationArray = ConfigData.get("NotificationArray", [])

    def SetConsole(self) -> None:
        title = "Roman Empire Reminder"

        if platform.system() == "Windows": 
            os.system("cls")
            os.system("title Roman Empire Reminder")
        else:
            os.system("clear")
            print(f'\33]0;{title}\a', end='', flush=True)

    def PrintHeader(self) -> None:
        print(r"""   
           ___                         ____           _           ___            _         __       
          / _ \___  __ _  ___ ____    / __/_ _  ___  (_)______   / _ \___ __ _  (_)__  ___/ /__ ____
         / , _/ _ \/  ' \/ _ `/ _ \  / _//  ' \/ _ \/ / __/ -_) / , _/ -_)  ' \/ / _ \/ _  / -_) __/
        /_/|_|\___/_/_/_/\_,_/_//_/ /___/_/_/_/ .__/_/_/  \__/ /_/|_|\__/_/_/_/_/_//_/\_,_/\__/_/   
                                             /_/                                                    
        """)
        print("Version: ?\nLast Updated: 7/8/2024\nCreator & Maintainer: Kendrick Fithen\nContributor(s): John Reed\n")

    def CheckOperatingSystem(self) -> None:
        if (platform.system() != "Windows" or platform.release() not in ["10", "11"]) and (platform.system() != "Linux"):
            print("You can't run this program on anything other than Linux (with dbus) or Windows 10/11. Sorry!")
            time.sleep(1)
            exit()
        
    def RandomizeIndex(self) -> None:
        self.NotificationIndex = random.randint(0, len(self.NotificationArray) - 1)

    def PrintReminder(self) -> None:
        CurrentDateTime = datetime.datetime.now()
        FormattedDateTime = CurrentDateTime.strftime("%m/%d/%y %H:%M:%S")
        print(FormattedDateTime + ": Reminded of the Roman Empire!")

    def PlayNotificationAudio(self) -> None:
        mixer.init()
        mixer.music.load(self.path / self.NotificationArray[self.NotificationIndex]["Audio"])
        mixer.music.play()
        mixer.music.get_pos

    def SayToastNotification(self) -> None:
        NotificationAudioLength = mixer.Sound(self.path / self.NotificationArray[self.NotificationIndex]["Audio"]).get_length()
        time.sleep(NotificationAudioLength)
        TextToSpeech = pyttsx3.init()
        TextToSpeech.say(self.NotificationArray[self.NotificationIndex]["Body"])
        TextToSpeech.runAndWait()

    def RemindOfRomanEmpire(self) -> None:
        self.RandomizeIndex()
        self.PrintReminder()
        notifier = GetNotifier(appName="Python")
        notification = Notification()
        notification.Icon = self.path / self.NotificationArray[self.NotificationIndex]["Image"]
        notification.Summary = self.NotificationArray[self.NotificationIndex]["Heading"]
        notification.Body = self.NotificationArray[self.NotificationIndex]["Body"]
        self.PlayNotificationAudio()
        notifier.Show(notification)
        self.SayToastNotification()


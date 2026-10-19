
import sys
import pathlib
rootPath = pathlib.Path(__file__).parent.parent
sys.path.append(str(rootPath))

import os
import time
import loguru

import src.Tools as Tools

loguru.logger.info(f"Current System is-> [{os.name}]")

gDNSIP = "127.0.0.1"

LogPath = os.path.join(rootPath, "log", "HttpDNSClient.log")

Round = 0

def doSync():
    global Round
    Round += 1
    loguru.logger.info(f"--------------- start to do Sync [{Round}] Times---------------")
    ip = Tools.GetGlobalIP()

    global gDNSIP
    loguru.logger.debug(f"Get back current ip - > [{ip}]")

    if ip is not None and gDNSIP != ip:
        loguru.logger.debug(f"ip[{ip}] is different to old[{gDNSIP}]")
        if Tools.UpdateDNS(ip):
            loguru.logger.debug(f"Domain Record updated ok.")
            gDNSIP = ip
        else:
            loguru.logger.error(f"Domain Record updated failed.")
    else:
        if ip == gDNSIP:
            loguru.logger.error(f"ip->[{ip}] is same with old[{gDNSIP}]")
        else:
            loguru.logger.error(f"ip->[{ip}], GetGlobalIP error")

if __name__ == "__main__":
    loguru.logger.debug("HttpDNS Update Start ...")
    loguru.logger.add(LogPath, rotation="1 day", retention="7 days", level="DEBUG")
    while(True):
        try:
            doSync()
        except Exception as e:
            loguru.logger.error(f"{e}")
        time.sleep(60)

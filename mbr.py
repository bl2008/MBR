import boto3
import os
import sys
import logging
from Backupworker import MyBackupWorker
#Backup job
def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Snapshot backup start.")
    lmybackupworker=MyBackupWorker()
    lmybackupworker.StartBackup()
    logger.info("Backup finish.")
    return

import logging
from Instances import MyInstances

#Instance discover job
def handler(event, context):
    gMyInstances = MyInstances()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Checking new Instance start.")
    gMyInstances.GetNewList()
    gMyInstances.GetOldList()
    gMyInstances.FindNewInstance()
    gMyInstances.SavetoBucket()
    logger.info("Checking new Instance finish.")
    return
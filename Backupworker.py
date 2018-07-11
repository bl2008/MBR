from Instances import MyInstances
from Instance import MyInstance

class MyBackupWorker:

    def __init__(self):
        return

    def StartBackup(self):
        lmyinstances = MyInstances()
        lmyinstances.GetOldList()
        for lid in lmyinstances.gOldInstanceIDList:
            #get instance
            lmyinstance=MyInstance(lid)
            #get instance volumes
            lmyinstance.GetVolumes()
            #create snapshot
            lmyinstance.CreateSnapshot()

# def main():
#     lmybackupworker=MyBackupWorker()
#     lmybackupworker.StartBackup()
#     return

# main()
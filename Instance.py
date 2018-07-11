import boto3
import botocore
import datetime


class MyInstance:
    gID = ""
    gvolumes = []
    gec2 = None
    gtimestamp = ""
    gname = ""

    def __init__(self, pid):
        self.gID = pid
        self.gec2 = boto3.resource('ec2')

        lcurrentDT = datetime.datetime.now()
        self.gtimestamp = lcurrentDT.strftime("%Y-%m-%d-%H-%M-%S")
        self.GetName()
        return

    def GetVolumes(self):
        linstance = self.gec2.Instance(self.gID)
        self.gvolumes = linstance.volumes.all()
        return

    def GetName(self):
        linstance = self.gec2.Instance(self.gID)
        for ltag in linstance.tags:
            if ltag['Key'] == 'Name':
                self.gname = ltag['Value']
                return
        self.gname = ""

    def CreateSnapshot(self):
        # freez xfs if possible, and the application IO.
        # pending code

        for lvolume in self.gvolumes:
            ldev=lvolume.attachments[0].get('Device')
            lname = self.gname + "-" + ldev.split("/")[2] + "-" + self.gtimestamp
            ltags = [{
                'ResourceType': 'snapshot',
                'Tags': [{'Key': 'Name', 'Value': lname},
                         {'Key': 'InstanceID', 'Value': self.gID},
                         {'Key': 'Mapdev', 'Value': ldev},
                         {'Key': 'Time', 'Value': self.gtimestamp}]
            }]
            lsnapshot = self.gec2.create_snapshot(VolumeId=lvolume.id,
                                                      Description="Snapshot backup by MBR",TagSpecifications=ltags)
        return


# test section
# lmyinstance = MyInstance('i-095542d07d57c61b3')
# lmyinstance.GetVolumes()
# for lv in lmyinstance.gvolumes:
#     print(lv.id)
# lmyinstance.GetName()
# lmyinstance.CreateSnapshot()
# print("done")

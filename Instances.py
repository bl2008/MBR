import boto3
import botocore
import json

class MyInstances:
    # New Instances ID list
    gNewInstanceIDList = []
    gOldInstanceIDList = []
    gBucketname = ""
    gListfilename = ""
    gFulllistcontent = {}

    def __init__(self):
        self.gBucketname = "bl2018backup"
        self.gListfilename = 'sys-backup/instances.json'
        return

    # Scan all instance and get the instance IDs
    def GetNewList(self):
        lec2 = boto3.resource('ec2')
        for linstance in lec2.instances.all():
            self.gNewInstanceIDList.append(linstance.id)
        return

    # iflistfile exist?
    def IfListfileexist(self):
        ls3 = boto3.resource('s3')
        try:
            ls3.Object(self.gBucketname, self.gListfilename).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # The object does not exist.
                return False
            else:
                # Something else has gone wrong.
                print("Read List file failed")
                exit(-111)
        else:
            # The object does exist.
            return True

    def GetOldList(self):
        if self.IfListfileexist():
            ls3 = boto3.resource('s3')
            lfile = ls3.Object(self.gBucketname, self.gListfilename)
            # pending read the content from json file in s3
            lbody = lfile.get()['Body'].read().decode('utf-8')
            self.gFulllistcontent = json.loads(lbody)
            for linstance in self.gFulllistcontent["Instances"]:
                self.gOldInstanceIDList.append(linstance["ID"])
        else:
            self.gOldInstanceIDList = []
            self.gFulllistcontent = {"Instances":[]}

    def FindNewInstance(self):
        for lnewinstanceid in self.gNewInstanceIDList:
            if lnewinstanceid in self.gOldInstanceIDList:
                continue
            else:
                # add new instance in Json list
                self.gOldInstanceIDList.append(lnewinstanceid)
                self.AddInstance(lnewinstanceid)

    def AddInstance(self, pid):
        lname=""
        lflag=""
        lec2 = boto3.resource('ec2')
        for ltag in lec2.Instance(pid).tags:
            if ltag["Key"]=="Name":
                lname=ltag["Value"]
            if ltag["Key"]=="IfBackup":
                lflag = ltag["Value"]
        lnewinstace = {"ID": pid, "Name": lname, "Backupornot": lflag}
        self.gFulllistcontent["Instances"].append(lnewinstace.copy())

    def SavetoBucket(self):
        ls3 = boto3.resource('s3')
        lbody = json.dumps(self.gFulllistcontent).encode()
        try:
            lbucket = ls3.Bucket(self.gBucketname)
            lbucket.put_object(ACL='private', ContentType='application/json', ContentEncoding='utf-8', Key=self.gListfilename, Body=lbody)
        except botocore.exceptions.ClientError as e:
            print("Write S3 list failed.")

    #def CheckBackupflag(self) #if Backupflag change to backup or not backup, update the list
# test section
# print("test start")
# gMyInstances = MyInstances()
# gMyInstances.GetNewList()
# print("current ec2 list: ", gMyInstances.gNewInstanceIDList)
# gMyInstances.GetOldList()
# print("s3 list:", gMyInstances.gOldInstanceIDList)
# gMyInstances.FindNewInstance()
# print("s3 list:", gMyInstances.gOldInstanceIDList)
#gMyInstances.SavetoBucket()

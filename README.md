# MBR
My backup and restore application for small AWS user (less than 50 instances)

SAM local test:
Discover Function:
sam local generate-event schedule|sam local invoke  --template template-discover.yaml MyDiscover

Backup Function:
sam local generate-event schedule|sam local invoke --template template.yaml MyBackup


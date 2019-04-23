import boto3
import sys


DRYRUN = True
IMAGE_ID = [sys.argv[1]]


ec2 = boto3.client('ec2')

# get snapshot ids
response_describe_images = ec2.describe_images(
    ImageIds=IMAGE_ID,
    DryRun=DRYRUN
)
print(response_describe_images)
snapshot_ids = []
for i in range(len(response_describe_images["Images"][0]["BlockDeviceMappings"])):
    snapshot_ids.append(response_describe_images["Images"][0]["BlockDeviceMappings"][i]["Ebs"]["SnapshotId"])
print(snapshot_ids)

# deregister ami
response_deregister_ami = ec2.deregister_image(
    ImageId=IMAGE_ID[0],
    DryRun=DRYRUN
)
print("Image deleted!")

# delete snapshots
for j in range(len(response_describe_images["Images"][0]["BlockDeviceMappings"])):
    response_delete_snapshots = ec2.delete_snapshot(
        SnapshotId=snapshot_ids[j],
        DryRun=DRYRUN
    )
print("Snapshot deleted!")


subnet="subnet-5874bf3f"

security_group="sg-503c6d18"

server_ec2_file=$(mktemp /tmp/server_ec2_file_XXXXX.json)
client_ec2_file=$(mktemp /tmp/client_ec2_file_XXXXX.json)
echo ${server_ec2_file}
echo ${client_ec2_file}

aws ec2 run-instances --image-id ami-432eb53c \
    --count 1 \
    --instance-type t2.nano \
    --key-name MyKeyPair \
    --security-group-ids ${security_group} \
    --subnet-id ${subnet} > ${server_ec2_file}
    
aws ec2 run-instances --image-id ami-432eb53c \
    --count 1 \
    --instance-type t2.nano \
    --key-name MyKeyPair \
    --security-group-ids ${security_group} \
    --subnet-id ${subnet} > ${client_ec2_file}


#jq '.' < ${server_ec2_file}

server_instance_id=$(jq -r '.Instances[0].InstanceId' < ${server_ec2_file})
client_instance_id=$(jq -r '.Instances[0].InstanceId' < ${client_ec2_file})

echo -e "Server ID : ${server_instance_id}"
echo -e "Client ID : ${client_instance_id}"

server_instance_desc_file=$(mktemp /tmp/server_ec2_desc_XXXXX.json)
client_instance_desc_file=$(mktemp /tmp/client_ec2_desc_XXXXX.json)

echo -e ${server_instance_desc_file}
echo -e ${client_instance_desc_file}

aws ec2 describe-instances --instance-ids ${server_instance_id} > ${server_instance_desc_file}
aws ec2 describe-instances --instance-ids ${client_instance_id} > ${client_instance_desc_file}

server_dns=$(jq -r '.Reservations[0].Instances[0].PublicDnsName' < ${server_instance_desc_file})
client_dns=$(jq -r '.Reservations[0].Instances[0].PublicDnsName' < ${client_instance_desc_file})

echo -e "Server : ${server_dns}"
echo -e "Client : ${client_dns}"

sleep 60

ssh -i "MyKeyPair.pem" ubuntu@${server_dns} -oStrictHostKeyChecking=no "echo \$(hostname)"
ssh -i "MyKeyPair.pem" ubuntu@${client_dns} -oStrictHostKeyChecking=no "echo \$(hostname)"




profiles_config = {
    "profile_name": "secop1",
    "profile_description": "seCop01",
    "region": "us-east-2",
    "az": "us-east-2b",
    "log_path": "/xcompute/test",
    "node_group_name": "test",
    "max_controllers": 5,
    "controller": {
        "iam": "arn:aws:iam::010438502665:instance-profile/xio-e2e-tests-xio-controller",
        "image_id": "ami-075953a1a858ea96f",
        "subnet_id": "subnet-06ed1d620d356fc17",
        "sg": "sg-06aa7e6da066b7e93",
        "instance_type": "c5d.xlarge",
        "volume_size": 100,
        "instance_tag_key": "exocop",
        "instance_tag_value": "xspot-controller"
    },
    "worker": {
        "iam": "arn:aws:iam::010438502665:instance-profile/xio-e2e-tests-xio-worker",
        "image_id": "ami-0684bf26ca8d316f7",
        "subnet_id": "subnet-06ed1d620d356fc17",
        "sg": "sg-06aa7e6da066b7e93",
        "instance_type": "m5",
        "instance_type_1": "m6i",
        "spot_fleet_type": "m5",
        "instance_tag_key": "exocop",
        "instance_tag_value": "xspot-worker"
    },
    "xspot": {
        "version": "xspot-3.1.3"
    }
}


environment_config = {
    "cluster_arn": "arn:aws:eks:us-west-2:374070299695:cluster/guru-k8s",
    "cluster_name": "guru-k8s",
    "setup_env_name": "pytestEnvXio1",

    "setup_PoolName_1": "pool-a",
    "setup_PoolSize_1": "10",
    "setup_ProfileName_1": "pytestXio1",
    "setup_CPUs_1": "2",
    "setup_ImageName_1": "k8s-129",
    "setup_MaxMemory_1": "4096",
    "setup_MinMemory_1": "4096",
    "setup_PrefixCount_1": "10",
    "setup_UserData_1": "",
    "setup_VolumeSize_1": "10",

    "setup_PoolName_2": "pool-b",
    "setup_PoolSize_2": "10",
    "setup_ProfileName_2": "pytestXio1",
    "setup_CPUs_2": "2",
    "setup_ImageName_2": "k8s-129",
    "setup_MaxMemory_2": "32500",
    "setup_MinMemory_2": "16900",
    "setup_PrefixCount_2": "10",
    "setup_UserData_2": "",
    "setup_VolumeSize_2": "10",

    "environment_type": "Amazon EKS",
    "environment_name": "seCopEnv01",

    "pool_name": "pool-se-a",
    "pool_name_1": "pool-se-b",
    "pool_size": "5",
    "profile_name": "seProf1",
    "profile_name_1": "az1",
    "image_name": "k8s-129",
    "cpus": "2",
    "min_memory": "4096",
    "max_memory": "4096",
    "volume_size": "20",
    "prefix_count": "4",
    "security_username": "k8s",
    "security_pemkey": "",
    "user_data": "echo Hello World"
}
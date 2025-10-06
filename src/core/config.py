import yaml

config = None
with open("config.yml", 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

#data base
host = config["database"]["host"]
port = config["database"]["port"]
user = config["database"]["user"]
password = config["database"]["password"]
name = config["database"]["name"]
schema = config["database"]["schema"]

#redis
host_redis = config["redis"]["host"]
port_redis = config["redis"]["port"]
db_redis = config["redis"]["db"]
ttl_redis = config["redis"]["ttl"]
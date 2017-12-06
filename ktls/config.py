import os

# current dir
CONFIG_PWD = os.path.dirname(os.path.realpath(__file__))

# root ca path
CONFIG_CERT = os.path.join(CONFIG_PWD, "ca", "cert.pem")

# root ca key
CONFIG_KEY = os.path.join(CONFIG_PWD, "ca", "key.pem")

# client ca path
CONFIG_CLIENT_CERT = os.path.join(CONFIG_PWD, "ca", "client.crt")

# client ca key
CONFIG_CLIENT_KEY = os.path.join(CONFIG_PWD, "ca", "client.key")

# cipher suite of ktls
CONFIG_CIPHER_SUITE = "ECDH-ECDSA-AES128-GCM-SHA256"

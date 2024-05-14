import paramiko
from paramiko import client, sftp_client

host = '172.21.0.0'
port = 22
user = 'test_user'
password = 'qwerty123!'

class SFTP:
    sftp: sftp_client.SFTPClient
    ssh: client.SSHClient
    host: str
    port: int
    user: str
    password: str

    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __enter__(self) -> sftp_client.SFTPClient:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(self.host, self.port, username=self.user, password=self.password)
        self.ssh = ssh
        sftp = ssh.open_sftp()
        self.sftp = sftp
        return sftp

    def __exit__(self, exc, _, __) -> bool:
        if exc is None:
            self.sftp.close()
            self.ssh.close()
            return True

        raise exc


with SFTP(host, port, user, password) as sftp:
    local_path = "test_file.txt"
    remote_path = "/test_folder/test_file.txt"
    sftp.put(local_path, remote_path)
    print('Success')

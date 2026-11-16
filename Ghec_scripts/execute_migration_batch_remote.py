import paramiko

def main():
    # SSH connection details
    hostname = '10.15.12.139'
    port = 22
    username = 'vxpala'
    password = 'summerTime665'

    # Local file path
    local_path = './migration-batch-05-08-2024-14.50.01.ps1'

    # Remote file path
    remote_path = '/tmp/migration-batch-05-08-2024-14.50.01.ps1'

    # Command to execute
    command = ''

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    # Copy file to remote server
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()

    command = "sudo su - "
    command = 'scp -P 122 /tmp/migration-batch-05-08-2024-14.50.01.ps1 admin@10.15.12.137:/tmp/migration-batch-05-08-2024-14.50.01.ps1'
    (stdin, stdout, stderr) = ssh.exec_command(command)
    # terminal = ssh.invoke_shell()
    # # terminal.send('junk')
    # terminal.send('ls')
    # import time
    # time.sleep(2)
    # output = terminal.recv(10240)
    # print(output)

    # "scp -P 122 /tmp/migration-batch-05-08-2024-14.50.01.ps1 admin@10.15.12.137:/tmp/migration-batch-05-08-2024-14.50.01.ps1"

    # Execute command remotely
    # stdin, stdout, stderr = ssh.exec_command(command)
    # output = stdout.read().decode('utf-8')
    # error = stderr.read().decode('utf-8')

    # print("Output:", output)
    # print("Error:", error)

    # Close SSH connection
    ssh.close()

main()
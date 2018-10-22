# Created by Lang Yu
# Oct 20, 2018
import paramiko
from paramiko.py3compat import input
import getpass
import os
import traceback
import socket

Port = 22
UseGSSAPI = False
DoGSSAPIKeyExchange = False

def open_remote_file(hostname, remote_filepath):
    # the func will return file_handler, connection(open)
    # note: please close connection after use
    username = "langyu"
    password = getpass.getpass("Password for %s@%s: " % (username, hostname))
    hostkeytype = None
    hostkey = None
    try:
        host_keys = paramiko.util.load_host_keys(
            os.path.expanduser("~/.ssh/known_hosts")
        )
    except IOError:
        try:
            # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
            host_keys = paramiko.util.load_host_keys(
                os.path.expanduser("~/ssh/known_hosts")
            )
        except IOError:
            print("*** Unable to open host keys file")
            host_keys = {}

    if hostname in host_keys:
        hostkeytype = host_keys[hostname].keys()[0]
        hostkey = host_keys[hostname][hostkeytype]
        print("Using host key of type %s" % hostkeytype)
    try:
        t = paramiko.Transport((hostname, Port))
        t.connect(
            hostkey,
            username,
            password,
            gss_host=socket.getfqdn(hostname),
            gss_auth=UseGSSAPI,
            gss_kex=DoGSSAPIKeyExchange,
        )
        sftp = paramiko.SFTPClient.from_transport(t)
        return sftp.open(remote_filepath), t
    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        exit(1)

def main():
    f, connection = open_remote_file("slurm.ttic.edu", "/home-nfs/langyu/demo_sftp_folder/demo_sftp.py")
    for line in f:
        print(line)
    connection.close()

if __name__ == '__main__':
    main()
import os
import time
import paramiko
import stat
import getpass
from pypers.steps.fetch.download.sftp_pk import SFTP_PK


class SFTP_CA(SFTP_PK): # using sftp_pk because of the walk function

    def connect(self):
        # Why should this be necessary ??? Changed the default_window_size for the sftp transport
        # source: https://stackoverflow.com/questions/45891553/paramiko-hangs-on-get-after-ownloading-20-mb-of-file")
        # getting files from sftp
        self.sftp_params = self.fetch_from['from_sftp']
        self.logger.info('getting %s files from sftp %s %s' % (
            'all' if self.limit == 0 else self.limit,
            self.sftp_params['sftp_server'],
            self.sftp_params['sftp_dir']))

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh.load_system_host_keys()

        self.ssh.connect(self.sftp_params['sftp_server'],
                         username=self.sftp_params['sftp_user'],
                         password=self.sftp_params['sftp_password'])
        t = self.ssh.get_transport()
        t.default_window_size = paramiko.common.MAX_WINDOW_SIZE
        t.packetizer.REKEY_BYTES = pow(2, 40)  # 1TB max, this is a security degradation!
        t.packetizer.REKEY_PACKETS = pow(2, 40)
        return self.ssh.open_sftp()

    def specific_process(self):
        self.output_files = []
        sftp = self.connect()

        print(self.sftp_params)
        sftp_dir = self.sftp_params['sftp_dir']
        self.logger.info('going to dir %s' % sftp_dir)
        sftp.chdir(sftp_dir)

        flist = []
        # looks for files recursively
        for path, files in self.sftp_walk(sftp, sftp_dir):
            for f in files:
                if self.rgx.match(f):
                    flist.append(os.path.join(path, f))

        # look for directories where files are present
        upload_dirs = []
        for f in flist:
            x = os.path.dirname(os.path.relpath(f, sftp_dir))
            if len(x) > 0:
                upload_dirs.append(x)
        upload_dirs.append(sftp_dir)

        # check if uploading is still active on every upload dir
        # print("Should test if the remote is still being updated in these locations: ["  + ",".join(upload_dirs)+"]")

        for upload_dir in set(upload_dirs):
            size_1 = sftp.stat(upload_dir).st_mtime
            time.sleep(self.sleep_secs)
            size_2 = sftp.stat(upload_dir).st_mtime

            if size_1 != size_2:
                sftp.close()
                self.ssh.close()
                raise Exception(
                    'SSH folder [%s] is HOT. Exit.' % os.path.join(sftp_dir,
                                                                   upload_dir))

            self.logger.info('SSH folder [%s] is cold' % os.path.join(
                sftp_dir, upload_dir))

        self.logger.info('get the files')


        # Preparation for fetching the archives one at a time
        sftp.close()
        self.ssh.close()

        count = 0
        reversed = True
        if self.limit:
            reversed = False
        for f in sorted(flist, reverse=reversed):
            filename = os.path.basename(f)  # 123.zip
            filepath = os.path.relpath(f, sftp_dir)  # dir/123.zip

            if self.limit and count == self.limit:
                break
            if filepath in self.done_archives:
                continue

            # Trying to fetch archives one at a time, if they are relevant
            # print("Connecting for " + filepath)
            sftp = self.connect()
            sftp.chdir(sftp_dir)

            count += 1
            self.logger.info('[sftp] %s: %s' % (count, f))

            dest_dir = os.path.join(self.output_dir, os.path.dirname(filepath))
            dest_file = os.path.join(dest_dir, filename)

            try:
                os.makedirs(dest_dir)
            except Exception as e:
                pass

            sftp.get(f, dest_file)
            self.output_files.append(dest_file)

            sftp.close()
            self.ssh.close()

        # sftp.close()
        # self.ssh.close()

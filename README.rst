bareos-fuse (bareosfs)
======================

Virtual Filesystem Showing Bareos Information

* uses https://github.com/bareos/python-bareos
* requires Bareos >= 15.2
* installation:

  * via pip:

    * ``pip install bareos-fuse``

      * (Note: The required Python package ``fuse-python`` requires a FUSE development files. On Debian make sure ``libfuse-dev`` is installed.)

Usage
-----

.. code:: console

  $ bareos-fuse.py --help
  Usage:
    Bareos Fuse filesystem: displays files from Bareos backups as a (userspace) filesystem.

    bareos-fuse.py [mountpoint] [options]

  Options:
    -h, --help             show this help message and exit
    -o opt,[opt...]        mount options
    -o address=BAREOS_DIRECTOR
                           address of the Bareos Director to connect [default:
                           "localhost"]
    -o port=PORT           address of the Bareos Director to connect [default:
                           "9101"]
    -o dirname=BAREOS_DIRECTOR_NAME
                           name of the Bareos Director to connect [default:
                           ""]
    -o name=BAREOS_CONSOLE_NAME
                           name of the Bareos Named Console. If not given, it
                           tries to use the Bareos Default Console
    -o password=PASSWORD   password of the Bareos Console to authenticate at
                           the Bareos Director
    -o restoreclient=BAREOS_CLIENT_NAME
                           Bareos client used to restore files
    -o restorejob=BAREOS_JOB_NAME
                           Bareos job used to restore files
    -o restorepath=PATH    path prefix to restore files [default:
                           "/var/cache/bareosfs/"]
    -o logfile=FILENAME    if given, log to FILENAME


Mount bareosfs via Bareos Default Console (without console name):

.. code:: console

   bareos-fuse.py -o address=localhost,password=secret /mnt


show job list
-------------


.. code:: console

  $ ls -la /mnt/jobs/all/
  drwxr-xr-x  5 root root 4096 Apr 23 22:12 jobid=128_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:12 jobid=129_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:15 jobid=131_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:12 jobid=133_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:17 jobid=135_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:18 jobid=137_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:15 jobid=139_level=F_status=T
  drwxr-xr-x  5 root root 4096 Apr 23 22:17 jobid=141_level=F_status=T
  ...


show volumes, including size and status
---------------------------------------

.. code:: console

  $ ls -la /mnt/volumes/
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0001
  -r--r-----  1 root root 1073693339 Sep 18 09:00 Full-0001=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0002
  -r--r-----  1 root root 1073678209 Sep 18 15:00 Full-0002=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0003
  -r--r-----  1 root root 1073685404 Sep 18 18:00 Full-0003=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0004
  -r--r-----  1 root root 1073728529 Sep 19 12:00 Full-0004=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0005
  -r--r-----  1 root root 1073709366 Sep 19 18:00 Full-0005=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0006
  -r--r-----  1 root root 1073729642 Sep 20 15:00 Full-0006=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0007
  -r--r-----  1 root root 1073702045 Sep 20 18:00 Full-0007=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0008
  -r--r-----  1 root root 1073712528 Sep 21 12:00 Full-0008=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0009
  -r--r-----  1 root root 1073684834 Sep 21 15:00 Full-0009=Full
  drwxr-xr-x  5 root root       4096 Jan  1  1970 Full-0010
  -rw-rw----  1 root root  732319090 Sep 22 15:00 Full-0010=Append


show content (files/directories) off a backup
---------------------------------------------

.. code:: console

  $ ls -la /mnt/clients/client1-fd/backups/jobid\=887_level\=F_status\=T/data/
  ...

restore files from a backup job
-------------------------------

Triggering restore is implemented using Extended Attributes.
This prevents, that a normal read access triggers a restore job.
To trigger a restore, set the extended attribute ``user.bareos.do`` of a file or directory  to ``restore``.

Note:
  * the mount parameter ``restoreclient`` is required for this operation. Otherwise you get a permission denied error.
  * the mount parameter ``restorejob`` is required, if you have more then one restore job defined.

Example for restoring all files of a full backup job:

.. code:: console

  $ cd /mnt/clients/client1-fd/backups/jobid\=887_level\=F_status\=T/data/
  $ getfattr -d .
  user.bareos.do
  user.bareos.do_options="mark | restore"
  user.bareos.restored="no"
  user.bareos.restorepath="/var/cache/bareosfs/jobid=887"
  $ setfattr -n user.bareos.do -v restore .
  $ getfattr -d .
  user.bareos.do="restore"
  user.bareos.do_options="mark | restore"
  user.bareos.restore_job_id="913"
  user.bareos.restored="yes"
  user.bareos.restorepath="/var/cache/bareosfs/jobid=887"


Files are now readable and links show there destination.

Instead of restoring all files and directories from the backup, you can set the "restore" value on individual files.
Each set will trigger a separate restore job.

# bareos-fuse (bareosfs)

Virtual Filesystem Showing Bareos Information

* uses https://github.com/bareos/python-bareos
* prebuild packages available at http://download.bareos.org/bareos/contrib/
* status: usable Proof of Concept

## Usage

```
/bin/bareos-fuse.py --help

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
    -o dirname=NAME        name of the Bareos Director to connect [default:
                           ""]
    -o name=NAME           name of the Bareos Named Console
    -o password=PASSWORD   password to authenticate at Bareos Director
                           [default: ""]
    -o logfile=FILENAME    if given, log to FILENAME
```

Mount bareosfs via Bareos Default Console (without console name):
```
mount -t bareosfs -o address=localhost,password=secret,logfile=/var/log/bareosfs.log fuse /mnt
```

## show job list
```
ls -la /mnt/jobs/all/
drwxr-xr-x  5 root root 4096 Apr 23 22:12 jobid=128_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:12 jobid=129_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:15 jobid=131_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:12 jobid=133_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:17 jobid=135_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:18 jobid=137_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:15 jobid=139_level=F_status=T
drwxr-xr-x  5 root root 4096 Apr 23 22:17 jobid=141_level=F_status=T
...
```

## show volumes, including size and status

```
ls -la /mnt/volumes/
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
```

## show content (files/directories) off a backup

```
ls -la /mnt/clients/paeffgen-fd/backups/jobid\=887_level\=F_status\=T/data/
...
```

# TODO:

* implement restore

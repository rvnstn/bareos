# bareos-fuse
Virtual Filesystem Showing Bareos Information




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


mount -t bareosfs -o address=localhost,password=secret,logfile=/var/log/bareosfs.log fuse /mnt

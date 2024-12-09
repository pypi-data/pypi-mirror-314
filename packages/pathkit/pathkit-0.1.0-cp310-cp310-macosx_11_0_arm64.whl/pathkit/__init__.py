try:
    from pathkit.ftp.path import FTPPath
except ImportError:
    pass

try:
    from pathkit.hdfs.path import HDFSPath
except ImportError:
    pass

try:
    from pathkit.local.path import LocalPath
except ImportError:
    pass

try:
    from pathkit.minio.path import MinIOPath
except ImportError:
    pass

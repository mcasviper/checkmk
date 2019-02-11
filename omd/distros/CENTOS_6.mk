DISTRO_CODE       = el6
OS_PACKAGES       =
OS_PACKAGES      += time # needed for mk-job
OS_PACKAGES      += traceroute # needed for Check_MK parent scan
OS_PACKAGES      += curl
OS_PACKAGES      += dialog
OS_PACKAGES      += expat
OS_PACKAGES      += graphviz
OS_PACKAGES      += graphviz-gd
OS_PACKAGES      += httpd
OS_PACKAGES      += libevent
OS_PACKAGES      += libtool-ltdl
OS_PACKAGES      += pango
OS_PACKAGES      += php
OS_PACKAGES      += php-cli
OS_PACKAGES      += php-xml
OS_PACKAGES      += php-mbstring
OS_PACKAGES      += php-pdo
OS_PACKAGES      += php-gd
OS_PACKAGES      += readline
OS_PACKAGES      += rsync
OS_PACKAGES      += rpcbind
OS_PACKAGES      += uuid
OS_PACKAGES      += xinetd
OS_PACKAGES      += cronie
OS_PACKAGES      += freeradius-utils
OS_PACKAGES      += perl-Time-HiRes # needed for PNP4Nagios
OS_PACKAGES      += libpcap # needed for ICMP of CMC
OS_PACKAGES      += glib2 # needed by msitools/Agent Bakery
OS_PACKAGES      += bind-utils # needed for check_dns
OS_PACKAGES      += poppler-utils # needed for preview of PDF in reporting
OS_PACKAGES      += libgsf # needed by msitools/Agent Bakery
OS_PACKAGES      += cpio # needed for Agent bakery (solaris pkgs)
OS_PACKAGES      += binutils # Needed by Check_MK Agent Bakery
OS_PACKAGES      += rpm-build # Needed by Check_MK Agent Bakery
#OS_PACKAGES      += pyOpenSSL # needed for Agent Bakery (deployment)
OS_PACKAGES       += libffi # needed for pyOpenSSL and dependant
USERADD_OPTIONS   = -M
ADD_USER_TO_GROUP = gpasswd -a %(user)s %(group)s
PACKAGE_INSTALL   = yum -y makecache ; yum -y install
ACTIVATE_INITSCRIPT = chkconfig --add %s && chkconfig %s on
APACHE_CONF_DIR   = /etc/httpd/conf.d
APACHE_INIT_NAME  = httpd
APACHE_USER       = apache
APACHE_GROUP      = apache
APACHE_BIN        = /usr/sbin/httpd
APACHE_CTL        = /usr/sbin/apachectl
APACHE_MODULE_DIR = /usr/lib/httpd/modules
APACHE_MODULE_DIR_64 = /usr/lib64/httpd/modules
HTPASSWD_BIN      = /usr/bin/htpasswd
PHP_FCGI_BIN      = /usr/bin/php-cgi
APACHE_ENMOD      = true %s
BECOME_ROOT       = su -c
MOUNT_OPTIONS     =
INIT_CMD          = /etc/init.d/%(name)s %(action)s

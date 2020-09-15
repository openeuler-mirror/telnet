Name:             telnet
Epoch:            1
Version:          0.17
Release:          77
Summary:          Client and Server programs for the Telnet communication protocol
License:          BSD
Url:              http://web.archive.org/web/20070819111735/www.hcs.harvard.edu/~dholland/computers/old-netkit.html
Source0:          ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-telnet-0.17.tar.gz
#sources form fedora/redhat
Source1:          telnet-client.tar.gz
Source2:          telnet@.service
Source3:          telnet.socket

#patches from fedora/redhat repositories
Patch0001:        telnet-client-cvs.patch
Patch0002:        telnetd-0.17.diff
Patch0003:        telnet-0.17-env.patch
Patch0004:        telnet-0.17-pek.patch
Patch0005:        telnet-0.17-issue.patch
Patch0006:        telnet-0.17-sa-01-49.patch
Patch0007:        telnet-0.17-8bit.patch
Patch0008:        telnet-0.17-argv.patch
Patch0009:        telnet-0.17-conf.patch
Patch0010:        telnet-0.17-cleanup_race.patch
Patch0011:        telnetd-0.17-pty_read.patch
Patch0012:        telnet-0.17-CAN-2005-468_469.patch
Patch0013:        telnet-gethostbyname.patch
Patch0014:        netkit-telnet-0.17-ipv6.diff
Patch0015:        netkit-telnet-0.17-nodns.patch
Patch0016:        telnet-0.17-errno_test_sys_bsd.patch
Patch0017:        netkit-telnet-0.17-reallynodns.patch
Patch0018:        telnet-rh678324.patch
Patch0019:        telnet-rh674942.patch
Patch0020:        telnet-rh704604.patch
Patch0021:        telnet-rh825946.patch
Patch0022:        telnet-0.17-force-ipv6-ipv4.patch
Patch0023:        netkit-telnet-0.17-core-dump.patch
Patch0024:        netkit-telnet-0.17-gcc7.patch
Patch0025:        netkit-telnet-0.17-manpage.patch
Patch0026:        netkit-telnet-0.17-telnetrc.patch
Patch0027:        CVE-2020-10188.patch

BuildRequires:    gcc-c++ ncurses-devel systemd
Requires:         systemd
Provides:         %{name}-server
Obsoletes:        %{name}-server

%description
Telnet is an application protocol used on the Internet or local area
network to provide a bidirectional interactive text-oriented communication
facility using a virtual terminal connection. The package includes a remote
login client program for telnet and a server daemon.

%package help
Summary: Help package for %{name}, including doc and man files.

%description help
This is the help package for %{name}. It includes a doc file and
some man files.

%prep
%setup -q -n netkit-telnet-%{version}
mv -f telnet telnet-NETKIT

%autosetup -T -D -a 1 -n netkit-telnet-%{version} -p1

%build
%{_configure} --with-c-compiler=gcc --prefix=%{_prefix} --exec-prefix=%{_exec_prefix}
sed -i 's,-O2,\$(CC_FLAGS),;s,LDFLAGS=.*,LDFLAGS=\$(LD_FLAGS),;s,^MANDIR=.*$,MANDIR=%{_mandir},' MCONFIG
sed -i 's,install [+-]s,install,g' ./telnet/GNUmakefile ./telnetd/Makefile ./telnetlogin/Makefile ./telnet-NETKIT/Makefile

%make_build CC_FLAGS="$RPM_OPT_FLAGS -fpie" LD_FLAGS="$LD_FLAGS -z now -pie"

%install
install -d %{buildroot}{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}
make install INSTALLROOT=%{buildroot}

install -Dpm644 %{SOURCE2} %{buildroot}%{_unitdir}/telnet@.service
install -pm644 %{SOURCE3} %{buildroot}%{_unitdir}/telnet.socket

%post
%systemd_post telnet.socket

%preun
%systemd_preun telnet.socket

%postun
%systemd_postun_with_restart telnet.socket

%files
%defattr(-,root,root,-)
%{_unitdir}/*
%{_sbindir}/in.telnetd
%{_bindir}/telnet

%files help
%defattr(-,root,root,-)
%doc README
%{_mandir}/man5/issue.net.5*
%{_mandir}/man8/in.telnetd.8*
%{_mandir}/man8/telnetd.8*
%{_mandir}/man1/telnet.1*

%changelog
* Fri Sep 11 2020 lunankun <lunankun@huawei.com> - 1:0.17-77
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix source0 url

* Mon Apr 27 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:0.17-76
- Type:cves
- ID:CVE-2020-10188
- SUG:restart
- DESC:fix CVE-2020-10188

* Sat Sep 14 2019 huzhiyu<huzhiyu1@huawei.com> - 1:0.17-75
- Package init

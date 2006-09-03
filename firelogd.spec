
%define		_ver	1.3
%define		_rev	5

Summary:	Firewall log analyzer and report generator
Summary(pl):	Analizator logów firewalla i generator raportów
Name:		firelogd
Version:	%{_ver}_%{_rev}
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://rouxdoo.freeshell.org/dmn/current/%{name}-%{_ver}-%{_rev}.tgz
# Source0-md5:	41c19fb70e25cf9da3a480b2da46e0ff
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-opt.patch
URL:		http://rouxdoo.freeshell.org/dmn/
BuildRequires:	ctags
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a program that will parse ipchains or netfilter (iptables) log
data in real time. It will queue up a small batch of alerts and mail
them to you. It can also be used to parse an existing log file and it
will take log data on standard input for formatting.

%description -l pl
To jest program, który przetwarza logi ipchains lub iptables w czasie
rzeczywistym. Kolejkuje kilka ostrze¿eñ i wysy³a je poczt±. Mo¿e byæ
tak¿e u¿yty do przetworzenia istniej±cego pliku logów i wy¶wietlenia
go w zadanym formacie.

%package scripts
Summary:	Scripts to run firelogd as daemon
Summary(pl):	Skrypty do uruchamiania firelogd jako demona
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description scripts
Scripts to run firelogd as daemon.

%description scripts -l pl
Skrypty do uruchamiania firelogd jako demona.

%prep
%setup -q -n %{name}-%{_ver}
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sysconfdir},/var/log} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install firelogd   $RPM_BUILD_ROOT%{_sbindir}
gzip -dc firelogd.8.gz > $RPM_BUILD_ROOT%{_mandir}/man8/firelogd.8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

mkfifo $RPM_BUILD_ROOT/var/log/kernelpipe

%clean
rm -rf $RPM_BUILD_ROOT

%post scripts
/sbin/chkconfig --add firelogd
if [ -f /var/lock/subsys/firelogd ]; then
	/etc/rc.d/init.d/firelogd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/firelogd start\" to start firelogd." >&2
	echo "Remember to configure syslogd to log kern.* to |/var/log/kernelpipe (fifo)." >&2
fi

%preun scripts
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/firelogd ]; then
		/etc/rc.d/init.d/firelogd stop
	fi
	/sbin/chkconfig --del firelogd
fi

%files
%defattr(644,root,root,755)
%doc README TEMPLATES BUGS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firelogd.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%files scripts
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) /var/log/kernelpipe

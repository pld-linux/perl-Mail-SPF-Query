#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%define	pdir	Mail
%define	pnam	SPF-Query
#
%include	/usr/lib/rpm/macros.perl
Summary:	Mail::SPF::Query - Perl implementation of SPF
Name:		perl-Mail-SPF-Query
Version:	1.97
Release:	2
# Same as perl
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	http://spf.pobox.com/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	486cdf385abfd413bc0c7923ea674b82
Source1:	spfd.init
URL: http://spf.pobox.com
BuildRequires:	perl-devel >= 5.6
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-Netmask
BuildRequires:	perl-URI

%if %{with tests}
BuildRequires:	perl-Test-Simple
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements a daemon to query SPF records for email forgery
detection.

%package -n spfd
Summary: SPF record checking daemon
Group: Networking/Daemons

%description -n spfd
SPF record checking daemon, operating as a local resolver on UNIX-domain
sockets

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/spfd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes
%{perl_vendorlib}/Mail/SPF/*.pm
%attr(755,root,root) %{_bindir}/spfquery
%{_mandir}/man3/*

%files -n spfd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/spfd
%attr(744,root,root) /etc/rc.d/init.d/spfd

%post -n spfd
/sbin/chkconfig --add spfd
umask 137
if [ -f /var/lock/subsys/spfd ]; then
        /etc/rc.d/init.d/spfd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/spfd start\" to start SPF daemon."
fi
 
%preun -n spfd
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/spfd ]; then
                /etc/rc.d/init.d/spfd stop 1>&2
        fi
        /sbin/chkconfig --del spfd
fi

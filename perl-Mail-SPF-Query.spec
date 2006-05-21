#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Mail
%define		pnam	SPF-Query
Summary:	Mail::SPF::Query - Perl implementation of SPF
Summary(pl):	Mail::SPF::Query - perlowa implementacja SPF
Name:		perl-Mail-SPF-Query
Version:	1.997
Release:	5
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://spf.pobox.com/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	9e110d00520e0fe174c25c0734a8baf6
Source1:	spfd.init
Patch0:		Mail-SPF-Query-spfd-host.patch
Patch1:		Mail-SPF-Query-spfd-detach.patch
URL:		http://spf.pobox.com/
%if %{with tests}
BuildRequires:	perl-Net-CIDR-Lite >= 0.15
BuildRequires:	perl-Net-DNS >= 0.33
BuildRequires:	perl-Net-Netmask
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-URI
%endif
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	perl(URI::Escape) >= 3.20
Requires:	perl-Net-CIDR-Lite >= 0.15
Requires:	perl-Net-DNS >= 0.33
Requires:	perl-Sys-Hostname-Long
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements a daemon to query SPF records for email forgery
detection.

%description -l pl
Ten modu³ jest implementacj± demona sprawdzaj±cego rekordy SPF w celu
wykrywania sfa³szowanej poczty.

%package -n spfd
Summary:	SPF record checking daemon
Summary(pl):	Demon sprawdzaj±cy rekordy SPF
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description -n spfd
SPF record checking daemon, operating as a local resolver on
UNIX-domain sockets.

%description -n spfd -l pl
Demon sprawdzaj±cy rekordy SPF, dzia³aj±cy jako lokalny resolver na
gniazdach uniksowych.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/spfd

%clean
rm -rf $RPM_BUILD_ROOT

%post -n spfd
/sbin/chkconfig --add spfd
%service spfd restart "SPF daemon"

%preun -n spfd
if [ "$1" = "0" ]; then
	%service spfd stop
	/sbin/chkconfig --del spfd
fi

%files
%defattr(644,root,root,755)
%doc Changes
%attr(755,root,root) %{_bindir}/spfquery
%dir %{perl_vendorlib}/Mail/SPF
%{perl_vendorlib}/Mail/SPF/*.pm
%{_mandir}/man3/*

%files -n spfd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/spfd
%attr(754,root,root) /etc/rc.d/init.d/spfd

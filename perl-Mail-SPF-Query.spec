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
Release:	1
# Same as perl
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	http://spf.pobox.com/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	486cdf385abfd413bc0c7923ea674b82
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorlib}/Mail/SPF/*.pm
%{_bindir}/*
%{_mandir}/man3/*

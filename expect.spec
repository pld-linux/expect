Summary:	Tcl extension
Summary(de):	Tcl-Erweiterung
Summary(fr):	Extension Tcl
Summary(pl):	Rozszerzenie Tcl
Summary(ru):	òÁÓÛÉÒÅÎÉÅ Tcl ÄÌÑ ÕÐÒÁ×ÌÅÎÉÑ ÐÒÏÇÒÁÍÍÁÍÉ ÉÚ ÓËÒÉÐÔÏ×
Summary(tr):	Programlar arasý etkileþimi mümkün kýlan Tcl geniþletmesi
Summary(uk):	òÏÚÛÉÒÅÎÎÑ Tcl ÄÌÑ ËÅÒÕ×ÁÎÎÑ ÐÒÏÇÒÁÍÁÍÉ Ú¦ ÓËÒÉÐÔ¦×
Name:		expect
%define	major	5.40
Version:	%{major}.0
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://expect.nist.gov/src/%{name}-%{version}.tar.gz
# Source0-md5:	6ae1b87c9af993a69b901b6e52962c18
Patch0:		%{name}-pty.patch
Patch1:		%{name}-alpha.patch
Patch2:		%{name}-bug7869.patch
Patch3:		%{name}-fixcat.patch
Patch4:		%{name}-jbj.patch
Patch5:		%{name}-soname.patch
Patch6:		%{name}-lib64.patch
Icon:		tcl.gif
URL:		http://expect.nist.gov/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	tcl-devel >= 8.4.6
BuildRequires:	tk-devel >= 8.4.6
Requires:	tcl >= 8.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	/usr/lib

%description
Expect is a tool for automating interactive applications such as
telnet, ftp, passwd, fsck, rlogin, tip, etc. It makes it easy for a
script to control another program and interact with it.

%description -l pl
Expect to narzêdzie do automatyzacji interakcji z aplikacjami takimi
jak telnet, ftp, passwd, fsck, rlogin, tip itp. Expect pozwala w ³atwy
sposób przy pomocy skryptu kontrolowaæ inny program.

%description -l de
Expect ist ein Tool zur Automatisierung interaktiver Applikationen wie
telnet, ftp, passwd, fsck, rlogin, tip usw. Mit seiner Hilfe kann ein
Skript ein anderes Programm sehr leicht steuern oder damit
interagieren.

%description -l fr
expect est un un outil pour automatiser les applications interactives
comme telnet, ftp, passwd, fsck, rlogin, tip, etc. Il est alors facile
pour un script de contrôler un autre programme et d'interagir avec
lui.

%description -l tr
Expect telnet, ftp, passwd, fsck, rlogin, tip gibi etkileþimli
uygulamalarý otomatize etmeye yarayan bir araçtýr. Bir uygulamanýn bir
diðer uygulamayý denetlemesini kolaylaþtýrýr.

%description -l ru
Expect - ÜÔÏ ÉÎÓÔÒÕÍÅÎÔ ÄÌÑ Á×ÔÏÍÁÔÉÚÁÃÉÉ ÉÎÔÅÒÁËÔÉ×ÎÙÈ ÐÒÏÇÒÁÍÍ,
ÔÁËÉÈ ËÁË telnet, ftp, passwd, fsck, rlogin, tip, É Ô.Ð. ðÏÚ×ÏÌÑÅÔ
ÕÐÒÁ×ÌÑÔØ ÐÒÏÇÒÁÍÍÁÍÉ É ×ÚÁÉÍÏÄÅÊÓÔ×Ï×ÁÔØ Ó ÎÉÍÉ ÉÚ ÓËÒÉÐÔÏ×.

%description -l uk
Expect - ÃÅ ¦ÎÓÔÒÕÍÅÎÔ ÄÌÑ Á×ÔÏÍÁÔÉÚÁÃ¦§ ¦ÎÔÅÒÁËÔÉ×ÎÉÈ ÐÒÏÇÒÁÍ, ÔÁËÉÈ
ÑË telnet, ftp, passwd, fsck, rlogin, tip, ¦ Ô.¦. äÏÚ×ÏÌÑ¤ ËÅÒÕ×ÁÔÉ
ÐÒÏÇÒÁÍÁÍÉ ÔÁ ×ÚÁ¤ÍÏÄ¦ÑÔÉ Ú ÎÉÍÉ Ú¦ ÓËÒÉÐÔ¦×.

%package X11
Summary:	Tk extension
Summary(pl):	Rozszerzenie Tk
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description X11
This package contains expectk, which is an Tk extension, just as
expect Tcl extension.

%description X11 -l pl
Ten pakiet zawiera expectk, który jest rozszerzeniem dla Tk takim jak
expect jest dla Tcl.

%package devel
Summary:	Tcl extension header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja do rozszerzenia jêzyka Tcl
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel >= 8.4.6

%description devel
Tcl extension language header files and develppment documentation.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do rozszerzenie jêzyka Tcl.

%package static
Summary:	Tcl extension static library
Summary(pl):	Biblioteka statyczna rozszerzenia jêzyka Tcl
Group:		Development/Languages/Tcl
Requires:	%{name}-devel = %{version}-%{release}

%description static
Tcl extension language static library.

%description static -l pl
Biblioteka statyczna rozszerzenia jêzyka Tcl.

%prep
%setup -q -n %{name}-%{major}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%ifarch amd64
%patch6 -p1
%endif

chmod +w {.,testsuite}/configure

%build
install /usr/share/automake/config.* .
# only local macros, don't call aclocal
%{__autoconf}
cd testsuite
cp ../aclocal.m4 .
%{__autoconf}
cd -
%configure \
	--enable-gcc \
	--enable-shared \
	--with-tclconfig=%{_ulibdir} \
	--with-tkconfig=%{_ulibdir} \
	--with-tclinclude=%{_includedir} \
	--with-tkinclude=%{_includedir}

cat expect_cf.h | sed "s|.*SETPGRP_VOID.*|\#define SETPGRP_VOID 1|" > expect_cf.h.new
mv -f expect_cf.h{.new,}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_bindir}/{rftp,rftp-expect}

ln -sf $(cd $RPM_BUILD_ROOT%{_libdir} ; echo libexpect%{major}.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libexpect%{major}.so
ln -sf $(cd $RPM_BUILD_ROOT%{_libdir} ; echo libexpect%{major}.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libexpect.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/autoexpect
%attr(755,root,root) %{_bindir}/autopasswd
%attr(755,root,root) %{_bindir}/cryptdir
%attr(755,root,root) %{_bindir}/decryptdir
%attr(755,root,root) %{_bindir}/dislocate
%attr(755,root,root) %{_bindir}/expect
%attr(755,root,root) %{_bindir}/ftp-rfc
%attr(755,root,root) %{_bindir}/kibitz
%attr(755,root,root) %{_bindir}/lpunlock
%attr(755,root,root) %{_bindir}/mkpasswd
%attr(755,root,root) %{_bindir}/passmass
%attr(755,root,root) %{_bindir}/rftp-expect
%attr(755,root,root) %{_bindir}/rlogin-cwd
%attr(755,root,root) %{_bindir}/timed-read
%attr(755,root,root) %{_bindir}/timed-run
%attr(755,root,root) %{_bindir}/unbuffer
%attr(755,root,root) %{_bindir}/weather
%dir %{_libdir}/expect*
%attr(755,root,root) %{_libdir}/expect*/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/libexpect*.so.*.*
%{_mandir}/man1/autoexpect.*
%{_mandir}/man1/cryptdir.*
%{_mandir}/man1/decryptdir.*
%{_mandir}/man1/dislocate.*
%{_mandir}/man1/expect.*
%{_mandir}/man1/kibitz.*
%{_mandir}/man1/mkpasswd.*
%{_mandir}/man1/passmass.*
%{_mandir}/man1/unbuffer.*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/expectk
%attr(755,root,root) %{_bindir}/multixterm
%attr(755,root,root) %{_bindir}/tknewsbiff
%attr(755,root,root) %{_bindir}/tkpasswd
%attr(755,root,root) %{_bindir}/xkibitz
%attr(755,root,root) %{_bindir}/xpstat
%{_mandir}/man1/expectk.*
%{_mandir}/man1/multixterm.*
%{_mandir}/man1/tknewsbiff.*
%{_mandir}/man1/xkibitz.*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog FAQ HISTORY NEWS README
%attr(755,root,root) %{_libdir}/libexpect*.so
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

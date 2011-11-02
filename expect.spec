#
# BIG FAT WARNING:
#	- expect requires mounted /dev/pts to avoid `spawn failed' errors.
#
%bcond_without	tests
Summary:	Tcl expect extension
Summary(de.UTF-8):	Tcl-Erweiterung
Summary(fr.UTF-8):	Extension Tcl
Summary(pl.UTF-8):	Rozszerzenie Tcl expect
Summary(ru.UTF-8):	Расширение Tcl для управления программами из скриптов
Summary(tr.UTF-8):	Programlar arası etkileşimi mümkün kılan Tcl genişletmesi
Summary(uk.UTF-8):	Розширення Tcl для керування програмами зі скриптів
Name:		expect
Version:	5.45
Release:	1
License:	BSD
Group:		Development/Languages/Tcl
Source0:	http://downloads.sourceforge.net/project/expect/Expect/%{version}/%{name}%{version}.tar.gz
# Source0-md5:	44e1a4f4c877e9ddc5a542dfa7ecc92b
Patch0:		%{name}-pty.patch
Patch1:		%{name}-bug7869.patch
Patch2:		%{name}-soname.patch
URL:		http://expect.nist.gov/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	tcl-devel >= 8.5.0
BuildRequires:	tk-devel >= 8.5.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
Requires:	tcl >= 8.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	/usr/lib

%description
Expect is a tool for automating interactive applications such as
telnet, ftp, passwd, fsck, rlogin, tip, etc. It makes it easy for a
script to control another program and interact with it.

%description -l pl.UTF-8
Expect to narzędzie do automatyzacji interakcji z aplikacjami takimi
jak telnet, ftp, passwd, fsck, rlogin, tip itp. Expect pozwala w łatwy
sposób przy pomocy skryptu kontrolować inny program.

%description -l de.UTF-8
Expect ist ein Tool zur Automatisierung interaktiver Applikationen wie
telnet, ftp, passwd, fsck, rlogin, tip usw. Mit seiner Hilfe kann ein
Skript ein anderes Programm sehr leicht steuern oder damit
interagieren.

%description -l fr.UTF-8
expect est un un outil pour automatiser les applications interactives
comme telnet, ftp, passwd, fsck, rlogin, tip, etc. Il est alors facile
pour un script de contrôler un autre programme et d'interagir avec
lui.

%description -l tr.UTF-8
Expect telnet, ftp, passwd, fsck, rlogin, tip gibi etkileşimli
uygulamaları otomatize etmeye yarayan bir araçtır. Bir uygulamanın bir
diğer uygulamayı denetlemesini kolaylaştırır.

%description -l ru.UTF-8
Expect - это инструмент для автоматизации интерактивных программ,
таких как telnet, ftp, passwd, fsck, rlogin, tip, и т.п. Позволяет
управлять программами и взаимодействовать с ними из скриптов.

%description -l uk.UTF-8
Expect - це інструмент для автоматизації інтерактивних програм, таких
як telnet, ftp, passwd, fsck, rlogin, tip, і т.і. Дозволяє керувати
програмами та взаємодіяти з ними зі скриптів.

%package X11
Summary:	Tk extension
Summary(pl.UTF-8):	Rozszerzenie Tk
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}

%description X11
This package contains expectk, which is an Tk extension, just as
expect Tcl extension.

%description X11 -l pl.UTF-8
Ten pakiet zawiera expectk, który jest rozszerzeniem dla Tk takim jak
expect jest dla Tcl.

%package devel
Summary:	Tcl expect extension header files and development documentation
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do rozszerzenia expect języka Tcl
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel >= 8.5.0
Obsoletes:	expect-static

%description devel
Tcl expect extension language header files and development
documentation.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja do rozszerzenia expect języka Tcl.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

chmod +w {.,testsuite}/configure

%build
install /usr/share/automake/config.* .
# only local macros, don't call aclocal
%{__autoconf}
cd testsuite
%{__autoconf} -I ..
cd ..
CFLAGS="%{rpmcflags} -I%{_includedir}/tcl-private/unix"
%configure \
%if "%{_lib}" == "lib64"
	--enable-64bit \
%endif
	--enable-gcc \
	--enable-shared \
	--with-tclconfig=%{_ulibdir} \
	--with-tkconfig=%{_ulibdir} \
	--with-tclinclude=%{_includedir} \
	--with-tkinclude=%{_includedir}

%{__make}

%{?with_tests:%{__make} test TCLSH_PROG=tclsh}

%install
rm -rf $RPM_BUILD_ROOT

LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	TCLSH_PROG=tclsh

mv -f $RPM_BUILD_ROOT%{_bindir}/{rftp,rftp-expect}

mv -f $RPM_BUILD_ROOT%{_libdir}/expect%{version}/libexpect%{version}.so $RPM_BUILD_ROOT%{_libdir}
ln -sf ../libexpect%{version}.so $RPM_BUILD_ROOT%{_libdir}/expect%{version}/libexpect%{version}.so
ln -sf libexpect%{version}.so $RPM_BUILD_ROOT%{_libdir}/libexpect.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HISTORY NEWS README
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
%attr(755,root,root) %{_libdir}/libexpect%{version}.so
%dir %{_libdir}/expect%{version}
%attr(755,root,root) %{_libdir}/expect%{version}/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/expect%{version}/libexpect%{version}.so
%{_mandir}/man1/autoexpect.1*
%{_mandir}/man1/cryptdir.1*
%{_mandir}/man1/decryptdir.1*
%{_mandir}/man1/dislocate.1*
%{_mandir}/man1/expect.1*
%{_mandir}/man1/kibitz.1*
%{_mandir}/man1/mkpasswd.1*
%{_mandir}/man1/passmass.1*
%{_mandir}/man1/unbuffer.1*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/multixterm
%attr(755,root,root) %{_bindir}/tknewsbiff
%attr(755,root,root) %{_bindir}/tkpasswd
%attr(755,root,root) %{_bindir}/xkibitz
%attr(755,root,root) %{_bindir}/xpstat
%{_mandir}/man1/multixterm.1*
%{_mandir}/man1/tknewsbiff.1*
%{_mandir}/man1/xkibitz.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexpect.so
%{_includedir}/expect*.h
%{_includedir}/tcldbg.h
%{_mandir}/man3/libexpect.3*

Summary:	tcl extension 
Summary(de):	tcl-Erweiterung 
Summary(fr):	Extension tcl 
Summary(pl):	Rozszerzenie TCL 
Summary(tr):	Programlar arasý etkileþimi mümkün kýlan tcl geniþletmesi
Name:		expect
Version:	5.32.2
Release:	49
License:	BSD
Group:		Development/Languages/Tcl
Group(de):	Entwicklung/Sprachen/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
Source0:	ftp://ftp.scriptics.com/pub/tcl/expect/%{name}.%{version}.tar.gz
Patch0:		%{name}-pty.patch
Patch1:		%{name}-alpha.patch
Patch2:		%{name}-bug7869.patch
Patch3:		%{name}-fixcat.patch
Patch4:		%{name}-jbj.patch
Icon:		tcl.gif
URL:		http://expect.nist.gov/
BuildRequires:	glibc-static
BuildRequires:	tcl-devel >= 8.3.2
BuildRequires:	tk-devel >= 8.3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package devel
Summary:	tcl extension header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja do rozszerzenia jêzyka TCL
Group:		Development/Languages/Tcl
Group(de):	Entwicklung/Sprachen/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
Requires:	%{name} = %{version}
Requires:	tcl-devel

%description devel
Tcl extension language header files and develppment documentation.

%description -l pl devel
Pliki nag³ówkowe i dokumentacja do rozszerzenie jêzyka TCL.

%package	static
Summary:	tcl extension static library
Summary(pl):	Biblioteka statyczna rozszerzenia jêzyka TCL
Group:		Development/Languages/Tcl
Group(de):	Entwicklung/Sprachen/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
Requires:	%{name}-devel = %{version}

%description static
Tcl extension language static library.

%description -l pl static
Biblioteka statyczna rozszerzenia jêzyka TCL.

%prep
%setup  -q -n %{name}5.32
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

chmod +w configure

%build
autoconf
%configure \
	--enable-gcc \
	--enable-shared \
	--with-tclconfig=%{_libdir} \
	--with-tkconfig=/%{_libdir} \
	--with-tclinclude=%{_includedir} \
	--with-tkinclude=%{_includedir}
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT

LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

( cd $RPM_BUILD_ROOT%{_bindir}; mv -f rftp rftp-expect )

gzip -9nf FAQ README ChangeLog

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/expect*
%attr(755,root,root) %{_libdir}/expect*/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/libe*.so
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc *.gz
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

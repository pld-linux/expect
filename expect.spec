Summary:	tcl extension 
Summary(de):	tcl-Erweiterung 
Summary(fr):	Extension tcl 
Summary(pl):	Rozszerzenie TCL 
Summary(tr):	Programlar aras� etkile�imi m�mk�n k�lan tcl geni�letmesi
Name:		expect
Version:	5.28
Release:	3
Copyright:	BSD
Group:		Development/Languages/Tcl
Group(pl):	Programowanie/J�zyki/Tcl
Source:		ftp://ftp.cme.nist.gov/pub/%{name}/%{name}.tar.gz
Icon:		tcl.gif
Patch0:		%{name}.patch
Patch1:		%{name}-mkpasswd.patch
Patch2:		%{name}-pty.patch
Patch3:		%{name}-strf.patch
Buildroot:	/tmp/%{name}-%{version}-root

%description
Expect is a tool for automating interactive applications such as
telnet, ftp, passwd, fsck, rlogin, tip, etc. It makes it easy for a
script to control another program and interact with it.

%description -l pl
Expect to narz�dzie do automatyzacji interakcji z aplikacjami 
takimi jak telnet, ftp, passwd, fsck, rlogin, tip itp. Expect
pozwala w �atwy spos�b przy pomocy skryptu kontrolowa� inny program.

%description -l de
Expect ist ein Tool zur Automatisierung interaktiver Applikationen 
wie telnet, ftp, passwd, fsck, rlogin, tip usw. Mit seiner Hilfe 
kann ein Skript ein anderes Programm sehr leicht steuern oder 
damit interagieren. 

%description -l fr
expect est un un outil pour automatiser les applications interactives
comme telnet, ftp, passwd, fsck, rlogin, tip, etc. Il est alors facile
pour un script de contr�ler un autre programme et d'interagir avec lui.

%description -l tr
Expect telnet, ftp, passwd, fsck, rlogin, tip gibi etkile�imli uygulamalar�
otomatize etmeye yarayan bir ara�t�r. Bir uygulaman�n bir di�er uygulamay�
denetlemesini kolayla�t�r�r.

%package	devel
Summary:	tcl extension header files and development documentation
Summary(pl):	Pliki nag��wkowe i dokumentacja do rozszerzenia j�zyka TCL
Group:		Development/Languages/Tcl
Group(pl):	Programowanie/J�zyki/Tcl
Requires:	%{name} = %{version}

%description devel
Tcl extension language header files and develppment documentation.

%description -l pl devel
Pliki nag��wkowe i dokumentacja do rozszerzenie j�zyka TCL.

%package	static
Summary:	tcl extension static library
Summary(pl):	Biblioteka statyczna rozszerzenia j�zyka TCL
Group:		Development/Languages/Tcl
Group(pl):	Programowanie/J�zyki/Tcl
Requires:	%{name}-devel = %{version}

%description static
Tcl extension language static library.

%description -l pl static
Biblioteka statyczna rozszerzenia j�zyka TCL.

%prep
%setup  -q
%patch0 -p1
%patch1 -p2
%patch2 -p1
%patch3 -p1

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS -w" \
./configure	--enable-gcc \
		--enable-shared \
		--prefix=/usr \
		--with-tclconfig=../tcl8.0.5/unix \
		--with-tkconfig=../tk8.0.5/unix \
		--with-tclinclude=../tcl8.0.5/generic \
		--with-tkinclude=../tk8.0.5/generic \
		--mandir=%{_mandir} %{_target_platform}
make 
cd ..

%install
rm -rf $RPM_BUILD_ROOT

LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} \
make \
    prefix=$RPM_BUILD_ROOT%{_prefix} \
    mandir=$RPM_BUILD_ROOT%{_mandir} \
    install

for n in $RPM_BUILD_ROOT/usr/bin/* ; do
	if head -1 $n | grep '#!'; then
		cp -a $n $n.in
		sed "s|$RPM_BUILD_ROOT||" < $n.in > $n
		rm -f $n.in
	fi
done

strip $RPM_BUILD_ROOT%{_bindir}/{expect,expectk}
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/*.so

( cd $RPM_BUILD_ROOT%{_bindir}; mv -f rftp rftp-expect )

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/man[13]/* FAQ README ChangeLog

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {FAQ,README,ChangeLog}.gz

%attr(755,root,root) %{_bindir}/*

%dir %{_libdir}/expect*
%attr(755,root,root) %{_libdir}/expect*/pkgIndex.tcl
%attr(755,root,root) %{_libdir}/libe*.so

%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)

%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)

%{_libdir}/*.a

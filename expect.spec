Summary:	tcl extension 
Summary(de):	tcl-Erweiterung 
Summary(fr):	Extension tcl 
Summary(pl):	Rozszerzenie TCL 
Summary(tr):	Programlar arasý etkileþimi mümkün kýlan tcl geniþletmesi
Name:		expect
Version:	5.28
Release:	3
Copyright:	BSD
Group:		Development/Languages/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
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
Expect to narzêdzie do automatyzacji interakcji z aplikacjami 
takimi jak telnet, ftp, passwd, fsck, rlogin, tip itp. Expect
pozwala w ³atwy sposób przy pomocy skryptu kontrolowaæ inny program.

%description -l de
Expect ist ein Tool zur Automatisierung interaktiver Applikationen 
wie telnet, ftp, passwd, fsck, rlogin, tip usw. Mit seiner Hilfe 
kann ein Skript ein anderes Programm sehr leicht steuern oder 
damit interagieren. 

%description -l fr
expect est un un outil pour automatiser les applications interactives
comme telnet, ftp, passwd, fsck, rlogin, tip, etc. Il est alors facile
pour un script de contrôler un autre programme et d'interagir avec lui.

%description -l tr
Expect telnet, ftp, passwd, fsck, rlogin, tip gibi etkileþimli uygulamalarý
otomatize etmeye yarayan bir araçtýr. Bir uygulamanýn bir diðer uygulamayý
denetlemesini kolaylaþtýrýr.

%package	devel
Summary:	tcl extension header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja do rozszerzenia jêzyka TCL
Group:		Development/Languages/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
Requires:	%{name} = %{version}

%description devel
Tcl extension language header files and develppment documentation.

%description -l pl devel
Pliki nag³ówkowe i dokumentacja do rozszerzenie jêzyka TCL.

%package	static
Summary:	tcl extension static library
Summary(pl):	Biblioteka statyczna rozszerzenia jêzyka TCL
Group:		Development/Languages/Tcl
Group(pl):	Programowanie/Jêzyki/Tcl
Requires:	%{name}-devel = %{version}

%description static
Tcl extension language static library.

%description -l pl static
Biblioteka statyczna rozszerzenia jêzyka TCL.

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

%changelog
* Sun Jan 31 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [5.28-1d]
- updated to 5.28,
- added Group(pl),
- compressed man pages && documentaction,

  by Maciej Ró¿ycki <macro@ds2.amg.gad.pl>
  
- added expect-mkpasswd.patch.  

* Thu Oct 08 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [5.26-2d]
- build against PLD Tornado,
- fixed pl translation,
- added %doc
- minor changes of the spec file.

* Sat Sep 26 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [5.26-2]
- added pl translation.

* Thu Sep  8 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [5.26-1]
- expect is now in separated source package from orher tcl/tk stuff,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- fixed using $RPM_OPT_FLAGS during compile (curren expect configure script
  don't accept passing CFLAGS in enviroment variable),
- added striping shared libraries and othet binary,
- added devel and static subpackage,
- added package icon,
- added %attr and %defattr macros in %files (allow build package from
  non-root account).

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed expect binaries exec permissions

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to Tix 4.1.0.006
- updated version numbers of tcl/tk to relflect includsion of p2

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tcl/tk to patch level 2
- updated tclX to 8.0.2

* Thu Oct 30 1997 Otto Hammersmith <otto@redhat.com>
- fixed filelist for tix... replacing path to the expect binary in scripts
  was leaving junk files around.

* Wed Oct 22 1997 Otto Hammersmith <otto@redhat.com>
- added patch to remove libieee test in configure.in for tcl and tk.
  Shoudln't be needed anymore for glibc systems, but this isn't the "proper" 
  solution for all systems
- fixed src urls

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- removed version numbers from descriptions

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to tcl/tk 8.0 and related versions of packages

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- fixed dangling tclx/tkx symlinks

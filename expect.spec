Summary:     tcl extension to allow interaction between programs and scripts
Summary(de): tcl-Erweiterung zur Ermöglichung der Interaktion zwischen  Programmen und Skripts 
Summary(fr): Extension tcl permettant l'intéraction entre programmes et scripts"
Summary(tr): Programlar arasý etkileþimi mümkün kýlan tcl geniþletmesi
Name:        expect
Version:     5.26
Release:     1
Copyright:   BSD
Group:       Development/Languages/Tcl
Source:      ftp://ftp.cme.nist.gov/pub/expect/expect.tar.gz
Icon:        tcl.gif
Patch:       expect.patch
Buildroot:   /tmp/%{name}-%{version}-root

%description
Expect is a tool for automating interactive applications such as
telnet, ftp, passwd, fsck, rlogin, tip, etc. It makes it easy for a
script to control another program and interact with it.

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

%package devel
Summary:     tcl extension header files and development documentation
Group:       Development/Languages/Tcl
Requires:    %{name} = %{version}

%description devel
Tcl extension language header files and develppment documentation.

%package static
Summary:     tcl extension static library
Group:       Development/Languages/Tcl
Requires:    %{name}-devel = %{version}

%description static
Tcl extension language static library.

%prep
%setup -q
%patch -p1

%build
# make the libraries reentrant
#RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_REENTRANT"

TCL_BIN_DIR=/usr/bin \
TCL_LIBRARY=/usr/lib \
CFLAGS="$RPM_OPT_FLAGS" \
./configure	--enable-gcc \
		--enable-shared \
		--prefix=/usr \
		--with-tclconfig=/usr/lib
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT/usr

LD_LIBRARY_PATH=$RPM_BUILD_ROOT/usr/lib \
make prefix=$RPM_BUILD_ROOT/usr install

strip $RPM_BUILD_ROOT/usr/{bin/*,lib/libe*.so} || :

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(755, root, root) /usr/bin/*
%dir /usr/lib/expect*
%attr(755, root, root) /usr/lib/expect*/pkgIndex.tcl
%attr(755, root, root) /usr/lib/libe*.so
%attr(644, root,  man) /usr/man/man1/*

%files devel
%attr(644, root, root) /usr/include/*
%attr(644, root,  man) /usr/man/man3/*

%files static
%attr(644, root, root) /usr/lib/lib*.a

%changelog
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

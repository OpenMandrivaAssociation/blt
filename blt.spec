Summary:	A Tk toolkit extension, including widgets, geometry managers, etc
Name:		blt
Version:	2.4z
Release:	29
License:	MIT
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/blt/
Source0:	BLT%{version}.tar.bz2
Source1:	%{name}.rpmlintrc
Patch0:		blt2.4z-patch-2.patch
Patch1:		blt2.4z-configure.in-disable-rpath.patch
Patch2:		blt2.4z-libdir.patch
Patch3:		blt2.4z-mkdir_p.patch
Patch4:		blt2.4z-64bit-fixes.patch
Patch5:		blt-2.4z-tcl8.5-fix.patch
# Loosens the version checking, or else it will fail when built against
# any Tcl/Tk with a minor version (8.5.1, 8.5.2, 8.5.3) - braindead test
# AdamW 2008/07
Patch6:		blt-2.4z-exact.patch
# Part fix, part kludge for Tcl 8.6 (interp->result, TIP #330) - AdamW
# 2008/12
Patch7:		blt-2.4z-tcl86.patch
Patch8:		blt-2.4z-tk8.6.patch
Patch9:		blt-2.4z-autoconf-fix.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	tk-devel
BuildRequires:	tcl-devel

%description
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

%prep
%setup -q -n %{name}%{version}
sed -i -e 's,local/,,g' demos/scripts/page.tcl
%patch0 -p1
%patch1 -p1 -b .rpath
%patch2 -p1 -b .libdir
%patch3 -p1 -b .mkdir_p
%patch4 -p1 -b .64bit-fixes
%patch5 -p1
%patch6 -p1 -b .exact
%patch7 -p1 -b .tcl86
%patch8 -p1 -b .tk8.6
%patch9 -p1 -b .autoconf~

autoconf

%build
%configure2_5x --libdir=%{tcl_sitearch}
make

%install
%makeinstall libdir=%{buildroot}%{tcl_sitearch}

ln -sf bltwish24 %{buildroot}%{_bindir}/bltwish
ln -sf bltsh24 %{buildroot}%{_bindir}/bltsh

# Dadou - 2.4u-2mdk - Don't put in %%_libdir things which should be in %%_docdir
rm -fr %{buildroot}%{tcl_sitearch}/blt2.4/NEWS
rm -fr %{buildroot}%{tcl_sitearch}/blt2.4/PROBLEMS
rm -fr %{buildroot}%{tcl_sitearch}/blt2.4/README
rm -fr %{buildroot}%{tcl_sitearch}/blt2.4/demos

# Dadou - 2.4u-2mdk - Prevent conflicts with other packages
for i in bitmap busy graph tabset tree watch; do
	mv %{buildroot}%{_mandir}/mann/$i{,-blt}.n
done

# need to be available as a shared lib as well as a tcl module
ln -sf %{tcl_sitearch}/libBLT24.so %{buildroot}%{_libdir}/libBLT24.so 
ln -sf %{tcl_sitearch}/libBLTlite24.so %{buildroot}%{_libdir}/libBLTlite24.so 

# development crap, we don't have anything that builds against this
# at present
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{tcl_sitearch}/*.a

%files
%doc MANIFEST NEWS PROBLEMS README
%doc examples/
%doc html/
%doc demos/
%{_bindir}/*
%{_mandir}/mann/*
%{_mandir}/man3/*
%{tcl_sitearch}/*.so
%{tcl_sitearch}/%{name}2.4
%{_libdir}/*.so


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4z-25
+ Revision: 663325
- mass rebuild

* Wed Mar 30 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.4z-24
+ Revision: 649288
- drop unused P8
- remove obsolete %%clean, buildroot, %%defattr etc.
- fix man page conflict with busy.n
- fix build with recent autoconf (P9)

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 2.4z-23
+ Revision: 635007
- rebuild
- tighten BR

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4z-22mdv2011.0
+ Revision: 603760
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4z-21mdv2010.1
+ Revision: 522211
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.4z-20mdv2010.0
+ Revision: 413175
- rebuild

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 2.4z-19mdv2009.1
+ Revision: 311075
- rebuild for new tcl
- drop all the ridiculous libification crap
- add tcl86.patch (fix build for tcl 8.6)
- add local.patch (fix a use of /usr/local)
- update libdir.patch
- spec clean

* Tue Jul 15 2008 Adam Williamson <awilliamson@mandriva.org> 2.4z-18mdv2009.0
+ Revision: 235704
- fix the symlinks to binaries (#40947)

* Mon Jul 14 2008 Adam Williamson <awilliamson@mandriva.org> 2.4z-17mdv2009.0
+ Revision: 235698
- add exact.patch: loosen the version checking in init to make it actually run

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2.4z-16mdv2009.0
+ Revision: 220484
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.4z-15mdv2008.1
+ Revision: 148966
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- buildrequires X11-devel instead of XFree86-devel

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 2.4z-14mdv2008.0
+ Revision: 82098
- use autoconf-2.13 explicitely
- rebuild for new soname of tcl

* Thu May 10 2007 Austin Acton <austin@mandriva.org> 2.4z-13mdv2008.0
+ Revision: 25852
- fix for tcl8.5


* Mon May 01 2006 Stefan van der Eijk <stefan@eijk.nu> 2.4z-12mdk
- rebuild for sparc

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4z-11mdk
- fix deps

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4z-10mdk
- rebuilt against soname aware deps

* Wed Feb 09 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4z-9mdk
- multiarch

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.4z-8mdk
- fix buildrequires
- wipe out buildroot before installing

* Fri Apr 23 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.4z-7mdk
- buildrequires

* Fri Dec 19 2003 Stefan van der Eijk <stefan@eijk.nu> 2.4z-6mdk
- remove redundant BuildRequires
- rebuild

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4z-5mdk
- Patch4: Some 64-bit fixes

* Mon Jul 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.4z-4mdk
- use %%mklibname macro


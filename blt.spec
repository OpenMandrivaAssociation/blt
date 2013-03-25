Summary:	A Tk toolkit extension, including widgets, geometry managers, etc
Name:		blt
Version:	2.4z
Release:	29
License:	MIT
Group:		System/Libraries
Url:		http://www.sourceforge.net/projects/blt/
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
Patch10:	blt-aarch64.patch
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(x11)

%description
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

%prep
%setup -qn %{name}%{version}
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
%patch10 -p1 -b .aarch64

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


Summary:	A Tk toolkit extension, including widgets, geometry managers, etc
Name:		blt
Version:	2.5.3
Release:	1
License:	MIT
Group:		System/Libraries
# Originally at http://www.sourceforge.net/projects/blt/ - but it looks like that
# has been abandoned ages ago
Url:		https://sourceforge.net/projects/wize/
Source0:	https://downloads.sourceforge.net/project/wize/blt-src-%{version}.zip
Source1:	%{name}.rpmlintrc
Patch1:		blt2.4z-configure.in-disable-rpath.patch
Patch2:		blt2.4z-libdir.patch
# Loosens the version checking, or else it will fail when built against
# any Tcl/Tk with a minor version (8.5.1, 8.5.2, 8.5.3) - braindead test
# AdamW 2008/07
Patch6:		blt-2.4z-exact.patch
# Part fix, part kludge for Tcl 8.6 (interp->result, TIP #330) - AdamW
# 2008/12
Patch7:		blt-2.4z-tcl86.patch
Patch8:		blt-2.4z-tk8.6.patch
Patch9:		blt-2.4z-autoconf-fix.patch
Patch10:	blt-2.5.3-compile.patch
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
%autosetup -p1 -n %{name}%(echo %{version}|cut -d. -f1-2)
sed -i -e 's,local/,,g' demos/scripts/page.tcl

autoconf

%build
# for some reason configure doesnt like CC being set (all file tests fail)
%configure --libdir=%{tcl_sitearch} --with-tcl=%{_libdir} --with-tk=%{_libdir} CC=''
%make_build -j1 LDFLAGS="%{build_ldflags}"

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}

make prefix=%{buildroot}%{_prefix} \
 exec_prefix=%{buildroot}%{_prefix} \
 bindir=%{buildroot}%{_bindir} \
 libdir=%{buildroot}%{tcl_sitearch} \
 includedir=%{buildroot}%{_includedir} \
 mandir=%{buildroot}%{_mandir} \
 scriptdir=%{buildroot}%{tcl_sitearch}/%{name}2.5 \
install

ln -sf bltwish25 %{buildroot}%{_bindir}/bltwish
ln -sf bltsh25 %{buildroot}%{_bindir}/bltsh

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
ln -sf %{tcl_sitearch}/libBLT25.so %{buildroot}%{_libdir}/libBLT25.so
ln -sf %{tcl_sitearch}/libBLTlite25.so %{buildroot}%{_libdir}/libBLTlite25.so

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
%doc %{_mandir}/mann/*
%doc %{_mandir}/man3/*
%{tcl_sitearch}/*.so
%{tcl_sitearch}/%{name}2.5
%{_libdir}/*.so

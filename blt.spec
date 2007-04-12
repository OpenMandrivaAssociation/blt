%define major 2
%define	libname	%mklibname %{name} %{major}
%define	libname_devel %mklibname %{name} %{major} -d

Summary:	A Tk toolkit extension, including widgets, geometry managers, etc
Name:		blt
Version:	2.4z
Release:	%mkrel 12
License:	MIT
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/blt/
Source0:	BLT%{version}.tar.bz2
Patch0:		blt2.4z-patch-2.patch
Patch1:		blt2.4z-configure.in-disable-rpath.patch
Patch2:		blt2.4z-libdir.patch
Patch3:		blt2.4z-mkdir_p.patch
Patch4:		blt2.4z-64bit-fixes.patch
Requires:	%libname
BuildRequires:	XFree86-devel
BuildRequires:	tk-devel
BuildRequires:	tcl-devel
BuildRequires:	autoconf2.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

%package	scripts
Summary:	TCL Libraries for BLT
Group:		System/Libraries

%description	scripts
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides TCL libraries needed to use BLT.

%package -n	%libname
Summary:	Shared libraries needed to use BLT
Group:		System/Libraries
Requires:	blt-scripts = %{version}

%description -n	%libname
BLT is an extension to the Tk toolkit. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to do any patching
of the Tcl or Tk source files to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides libraries needed to use BLT.

%package -n	%libname_devel
Summary:	Headers of BLT
Group:		Development/Other
Requires:	%libname = %version-%release
Provides:	lib%name-devel = %version-%release
Obsoletes:	blt-devel
Provides:	blt-devel

%description -n	%libname_devel
BLT is an extension to the Tk toolkiy. BLT's most useful feature is the
provision of more widgets for Tk, but it also provides more geometry managers
and miscellaneous other commands. Note that you won't need to any patching
of the Tcl or Tk source file to use BLT, but you will need to have Tcl/Tk
installed in order to use BLT.

This package provides headers needed to build packages based on BLT.

%prep
%setup -q -n %name%version
%patch0 -p1
%patch1 -p1 -b .rpath
%patch2 -p1 -b .libdir
%patch3 -p1 -b .mkdir_p
%patch4 -p1 -b .64bit-fixes
autoconf

%build
%configure
make 

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

ln -sf libBLT.so.2.4 $RPM_BUILD_ROOT%_libdir/libBLT.so
ln -sf libBLTlite.so.2.4 $RPM_BUILD_ROOT%_libdir/libBLTlite.so
ln -sf bltwish-2.4 $RPM_BUILD_ROOT%_bindir/bltwish
ln -sf bltsh-2.4 $RPM_BUILD_ROOT%_bindir/bltsh

# Dadou - 2.4u-2mdk - Don't put in %%_libdir things which should be in %%_docdir
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/demos
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/NEWS
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/PROBLEMS
rm -fr $RPM_BUILD_ROOT/%_prefix/lib/blt2.4/README

# Dadou - 2.4u-2mdk - Remove +x permissions in %%_docdir to be sure that RPM
#                     will don't want some strange dependencies
perl -pi -e "s|local/||" $RPM_BUILD_DIR/%name%version/demos/scripts/page.tcl
perl -pi -e "s|local/||" $RPM_BUILD_DIR/%name%version/html/hiertable.html

# Dadou - 2.4u-2mdk - Prevent conflicts with other packages
for i in bitmap graph tabset tree watch; do
	mv $RPM_BUILD_ROOT/%_mandir/mann/$i{,-blt}.n
done

%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/bltHash.h

%clean
rm -fr $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc MANIFEST NEWS PROBLEMS README
%doc demos/
%doc examples/
%doc html/
%_bindir/*
%_mandir/mann/*
%_mandir/man3/*

%files scripts
%defattr(-,root,root,-)
%doc MANIFEST NEWS PROBLEMS README
%dir %{_prefix}/lib/blt2.4
%{_prefix}/lib/blt2.4/*

%files -n %libname
%defattr(-,root,root,-)
%_libdir/*.so

%files -n %libname_devel
%defattr(-,root,root,-)
%_includedir/*.h
%multiarch %{multiarch_includedir}/*.h
%_libdir/*.a


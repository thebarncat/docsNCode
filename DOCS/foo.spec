Summary: foo stuff 
%define version 1.17 
Name: jikes 
Prefix: /usr 
Provides: jikes 
Release: 1 
Source: foo-%{version}.tar.gz 
# needed shell scipr
Source1: foo.sh
Patch0: foo-fix1.patch
URL: http://foo.com
Version: %{version} 
Packager: Jim Kipp  
Buildroot: /tmp/foo/%{name}-root 
#Buildroot: %{_tmppath}/%{name}-%{version}-root 
BuildRequires: ncurses-devel
#define a macro. today will expand to the shell cmd
%define today %(date) 
%description 
This is test build RPM 

%prep 
# -q turns of verbose
#changes to the build directory, typically /usr/src/redhat/BUILD, and then extracts the source files
%setup -q 
# apply patch 1 see man patch for options
%patch0 -p1 -b .sh 


%build 
%configure
#check pg 30 of rpm guid for options
#./configure CXXFLAGS=-O3 --prefix=$RPM_BUILD_ROOT/usr 
# specoify a different prefixe dir
#./configure --prefix=$RPM_BUILD_ROOT/usr 
make 

%install 
# check pg 30 of rpm guid for options
# see install strip and make man pages
rm -fr $RPM_BUILD_ROOT 
make install 
# make install PREFIX=$RPM_BUILD_ROOT/usr 

%clean 
rm -rf $RPM_BUILD_ROOT 

%files 
# specify defualt ownership and perms for all files in pkg
# the '-' leaves the perms section as is 
%defattr(-,root,root) 
# packag single file
/usr/bin/foo 
# pacakge all files withing the $RPM_BUILD_ROOT/usr/bin dir
/usr/bin/*
# allows you to control the permissions for a particular file
%attr(0644, root, root) /etc/foo.conf 
%doc /usr/doc/foo-%{version}/license.htm 
%doc /usr/man/man1/foo.1* 
%doc README NEWS 
# pacakge all files withing the $RPM_BUILD_ROOT/usr/share/man/man1 dir 
%{_mandir}/man1/*
%config /etc/rc.d/init.d/* 
%config /etc/foo.conf 

# a script run prior to installation, pre, and a script run after installation, %post.
# The same concepts apply when a package is erased, or uninstalled.
# The preun script is run just before the uninstall and the %postun script just after the uninstall
# the %pre script is rarely used.
%post
/sbin/chkconfig --add foo

%preun
# $1 is the count of the number of this pkg is installed
if [ "$1" = 0 ] ; then
/sbin/service foo stop > /dev/null 2>&1
/sbin/chkconfig --del foo
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
/sbin/service foo condrestart > /dev/null 2>&1
fi
exit 0

%changelog 
* Fri Jun 21 2002 jim kipp 
- Downloaded version 1.4, applied patches 
* Tue May 08 2001 jim kipp 
- updated to 1.3





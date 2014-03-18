# TODO
# - fix testing

# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# build without tests

%include	/usr/lib/rpm/macros.java
Summary:	Framework for running Java from the cli without the JVM startup overhead
Name:		nailgun
Version:	0.7.1
Release:	0.1
License:	Apache v2.0
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/nailgun/%{name}-src-%{version}.zip
# Source0-md5:	79365e339275d774b7c5c8b17b7ece40
URL:		http://martiansoftware.com/nailgun/
Patch0:		remove-tools-jar-dependencies.patch
Patch1:		notestdep.patch
BuildRequires:	ant
%{?with_tests:BuildRequires:	ant-junit}
BuildRequires:	jdk
BuildRequires:	jpackage-utils
Requires:	jpackage-utils
Requires:	jre
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nailgun is a client, protocol, and server for running Java programs
from the command line without incurring the JVM startup overhead.
Programs run in the server (which is implemented in Java), and are
triggered by the client (written in C), which handles all I/O.

%package javadoc
Summary:	Javadocs for %{name}
Group:		Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

find -name '*.jar' | xargs rm -v

%build
%ant compile-server jar %{?with_tests:test} %{?with_apidocs:javadoc}

# rebuild with our cflags
%{__cc} -Wall -pedantic %{rpmcppflags} %{rpmcflags} %{rpmldflags} -o ng src/c/ng.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_bindir}}

cp -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -p ng $RPM_BUILD_ROOT%{_bindir}/ng

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt
%{_javadir}/nailgun.jar
%attr(755,root,root) %{_bindir}/ng

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif

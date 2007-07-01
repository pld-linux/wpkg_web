#TODO - scripts,database,config
Summary:	WPKG web Interface
Summary(pl.UTF-8): Interfejs WWW dla WPKG
Name:		wpkg_web
Version:	1.1.0
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://wpkg.linuxkidd.com/download/%{name}-%{version}-b.tgz
# Source0-md5:	48d0fc041dce1c081e7999d360f4d5bf
URL:		http://wpkg.linuxkidd.com/
BuildRequires:	rpm-perlprov
BuildRequires:  rpmbuild(macros) >= 1.268
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	php-cli
Requires:	webserver
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
WPKG-web - interface was created to ease the use of WPKG, a great
Software distribution and update tool designed to help Windows
Administrators.

%prep
%setup -q

# undos the source
find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

# remove svn control files
find -name .svn -print0 | xargs -0 rm -rf

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/{scripts,include,grafx,db},%{_sysconfdir}}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
install *.{php,css,js} $RPM_BUILD_ROOT%{_appdir}
install scripts/* $RPM_BUILD_ROOT%{_appdir}/scripts
install include/*.php $RPM_BUILD_ROOT%{_appdir}/include
install db/*.sql $RPM_BUILD_ROOT%{_appdir}/db
cp -rf grafx $RPM_BUILD_ROOT%{_appdir}/grafx
 
%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL
%attr(750,root,http) %dir %{_appdir}/
%{_appdir}/*
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*

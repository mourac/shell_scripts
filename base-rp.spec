# spec file for package base-pr
#
Name:		base-pr
Version:        %(../rpm_version)
Release:        %(../rpm_release)%{?tempdb:.tempdb}%{?sql2005:.sql2005}
License:	MyCompany
Summary:	kirayi tomcat base directories and config files in them
Group:		Productivity/Networking/Web
Provides:	base-pr
Requires:	tomcat >= 7.0.39
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define _sysconfdir  /etc
%define currentDir   %(pwd)
%define _pr          %{currentDir}/pr

%if 0%{?tempdb:1}
%define dbsuffix _DB_SUFFIX=_Temp
%else
%define dbsuffix _DB_SUFFIX:
%endif

%if 0%{?sql2005:1}
%define _sqljarfile sqljdbc.jar
%else
%define _sqljarfile sqljdbc4.jar
%endif

%description
rp-base provides configuration for kirayi server in 
/etc/tomcat/pr,
directory structure in in /srv/www/tomcat/pr.
branch=%(git rev-parse --abbrev-ref HEAD)
commit=%(git rev-parse HEAD)

%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT%{_var}/log/tomcat/pr
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/tomcat/pr
install -m 755 -d $RPM_BUILD_ROOT/srv/www/tomcat/pr

# configuration for pr
(cd %{_pr} ; tar cf - . --exclude .hg --exclude \*~) | \
  tar xf - -C $RPM_BUILD_ROOT%{_sysconfdir}/tomcat/pr
chmod 400 $RPM_BUILD_ROOT%{_sysconfdir}/tomcat/pr/*.m4
ln -sf %{_sysconfdir}/tomcat/pr $RPM_BUILD_ROOT/srv/www/tomcat/pr/conf

# log for pr
install -m 755 -d $RPM_BUILD_ROOT%{_var}/log/tomcat/pr/ptBins
ln -sf %{_var}/log/tomcat/pr $RPM_BUILD_ROOT/srv/www/tomcat/pr/logs

# work for pr
install -m 755 -d $RPM_BUILD_ROOT%{_var}/cache/tomcat/pr
ln -sf %{_var}/cache/tomcat/pr $RPM_BUILD_ROOT/srv/www/tomcat/pr/work

# temp for pr
install -m 755 -d  $RPM_BUILD_ROOT/srv/www/tomcat/pr/temp

# webapps for pr (empty to prevent double instances)
install -m 755 -d $RPM_BUILD_ROOT/srv/www/tomcat/pr/webapps

# setenv.sh in $CATALINA_BASE/bin
install -m 755 -d $RPM_BUILD_ROOT/srv/www/tomcat/pr/bin
cp %{_pr}/../setenv.sh $RPM_BUILD_ROOT/srv/www/tomcat/pr/bin/setenv.sh

# cron to compress old logs
install -m 755 -d $RPM_BUILD_ROOT/etc/cron.daily
cp %{_pr}/../dailyApp-log-compress $RPM_BUILD_ROOT/etc/cron.daily/dailyApp-log-compress
cp %{_pr}/../sanitize-log $RPM_BUILD_ROOT/etc/cron.daily/sanitize-log

# SQL JDBC driver
install -m 755 -d $RPM_BUILD_ROOT/usr/share/tomcat/lib
cp %{_pr}/../%{_sqljarfile} $RPM_BUILD_ROOT/usr/share/tomcat/lib/%{_sqljarfile}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ ! -f /etc/sysconfig/xyz-db-user.m4 ]
then
        echo "/etc/sysconfig/xyz-db-user.m4 file with user credentials does not exist, bailing out"
        exit 2
fi

%post
cat >/etc/sysconfig/tomcat/env/CATALINA_BASE <<_CB
/srv/www/tomcat/pr
_CB

if [ -f /etc/sysconfig/xxx ]; then
  . /etc/sysconfig/xxx

  cd /srv/www/tomcat/pr/conf

  m4 --define=%{dbsuffix} context.xml.${MYCOMPANY_ENVIRONMENT}.m4 > context.xml
  m4 server.xml.m4 > server.xml
  chown tomcat:tomcat context.xml server.xml
  chmod 400 context.xml server.xml

  svc -du /service/tomcat
else
  echo "/etc/sysconfig/xxx does not exist, looks fishy, bailing out..."
  exit 1
fi


%files
%attr(-, tomcat, tomcat) /srv/www/tomcat/pr
%dir %attr(-, tomcat, tomcat) %{_sysconfdir}/tomcat/pr
%config %attr(-, tomcat, tomcat) %{_sysconfdir}/tomcat/pr/*
#%attr(400,root,root) %{_sysconfdir}/tomcat/pr/context.xml.*.m4
%attr(-, tomcat, tomcat) %{_var}/log/tomcat/pr
%attr(-, tomcat, tomcat) %{_var}/cache/tomcat/pr
%attr(550, root, root) /etc/cron.daily/dailyApp-log-compress
%attr(550, root, root) /etc/cron.daily/sanitize-log
%attr(444, root, root) /usr/share/tomcat/lib/%{_sqljarfile}

%changelog


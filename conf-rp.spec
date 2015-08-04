#
# spec file for package conf-pr
#

Name:           conf-pr
Version:        %(../rpm_version)
Release:        %(../rpm_release)
License:        MyCompany
Summary:        rp kirayi configuration files
Group:          Productivity/Networking/Web
Provides:       conf-pr
Requires:       tomcat >= 7.0.25
Requires:       base-pr
Requires:       m4
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define currentDir   %(pwd)
%define repoDir	     %{currentDir}/../../..
%define baseDir      %{repoDir}/domestic/kirayi_src/src/main/resources/config/
%define sourceroot   ~/build/%{name}
%define _source_dir  %{repoDir}/build/confs/conf-pr/conf
%define _erp         /home/webapps/erentpayer
%define _pr          /home/webapps/kirayi
%define _pr_conf     %{_pr}/conf
%define _sysconfdir  /etc
%define __spec_install_post /usr/lib/rpm/brp-compress

%description
conf-pr provides horrible configuration files in %{_pr_conf}
branch=%(git rev-parse --abbrev-ref HEAD)
commit=%(git rev-parse HEAD)

%prep
my_root=%{sourceroot}
rm -rf ${my_root}
mkdir -p ${my_root}
rm -rf ${my_root}
cp -r %{_source_dir}/ ${my_root}/

for m_dir in xml xsl st
do
  rm -rf ${my_root}/${m_dir}
  cp -r %{baseDir}${m_dir} ${my_root}/${m_dir}
done
rm -rf ${my_root}/*.drl
rm -rf ${my_root}/rules/*.drl
cp -r %{baseDir}rules/RP/ ${my_root}/rules/

# drools.changeset_url
rm -rf ${my_root}/change-set-1.0.0.xsd
cp -r %{baseDir}change-set-1.0.0.xsd ${my_root}/change-set-1.0.0.xsd

%install
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT%{_pr_conf}
cp -a %{sourceroot}/* $RPM_BUILD_ROOT%{_pr_conf}
rm -f $RPM_BUILD_ROOT%{_pr_conf}/*~
rm -f $RPM_BUILD_ROOT%{_pr_conf}/*.orig
ln -sf /var/log/tomcat/pr/ $RPM_BUILD_ROOT%{_pr}/logs
install -m 755 -d $RPM_BUILD_ROOT%{_pr}/index
install -m 755 -d $RPM_BUILD_ROOT%{_pr}/import/importlog
install -m 755 -d $RPM_BUILD_ROOT%{_pr}/import/importlog_backup
install -m 755 -d $RPM_BUILD_ROOT%{_pr}/import/importtracker
install -m 755 -d $RPM_BUILD_ROOT%{_pr}/import/importtracker_backup

install -m 755 -d $RPM_BUILD_ROOT%{_erp}/atHome
install -m 755 -d $RPM_BUILD_ROOT%{_erp}/fab
install -m 755 -d $RPM_BUILD_ROOT%{_erp}/atHome/jenark
install -m 755 -d $RPM_BUILD_ROOT%{_erp}/atHome/new
install -m 755 -d $RPM_BUILD_ROOT%{_erp}/atHome/old
install -m 755 -d $RPM_BUILD_ROOT%{_erp}/atHome/temp
install -m 755 -d $RPM_BUILD_ROOT%{_erp}/atHome/jenark/old

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ -f /etc/sysconfig/xxx ]; then
  . /etc/sysconfig/xxx

  cd %{_pr_conf}

  if [ -f kirayi_root.properties ]; then
       mv kirayi_root.properties \
          kirayi_root.properties-$(date +%Y%m%d%H%M)
  fi
  m4 properties.m4 \
     host-kirayi_root.properties \
     env-kirayi_root.properties.${MYCOMPANY_ENVIRONMENT} \
     common-kirayi_root.properties \
   > kirayi_root.properties
   
   m4 properties.m4 \
      frosting.properties.${MYCOMPANY_ENVIRONMENT} \
      > frosting.properties 

  if [ ! -f bin.txt ]; then
    cp bin.txt.seed bin.txt
  fi

   chown tomcat:tomcat kirayi_root.properties frosting.properties hibernate.cfg.xml bin.txt

  svc -du /service/tomcat
else
  echo "/etc/sysconfig/xxx does not exist, looks fishy, bailing out..."
  exit 1
fi

%files
%attr(-, tomcat, tomcat) %{_pr}
%attr(-, tomcat, tomcat) %{_erp}

%changelog


# spec file for html files of the www.rentbytext.com site

Name:           PAY_rp_rentbytext
Version:        %(../rpm_version)
Release:        %(../rpm_release)
License:        MyCompany
Summary:        MyCompany rentbytext.com html
Group:          Web/MarketingFiles
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Prefix:         /usr

%define currentDir   %(pwd)
%define repoDir      %{currentDir}/../../..
%define baseDir      %{repoDir}/static
%define sourceroot   ~/build/%{name}
%define destroot     /srv/data/content/rentbytext.com
%define __spec_install_post /usr/lib/rpm/brp-compress

%description
html files for kirayi.com
branch=%(git rev-parse --abbrev-ref HEAD)
commit=%(git rev-parse HEAD)

%prep
my_root=%{sourceroot}
rm -rf ${my_root}
mkdir -p ${my_root}
cp -r %{baseDir}/domestic/rentbytext.com/* ${my_root}/

%build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && \
   rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{destroot}
cp -a %{sourceroot}/* $RPM_BUILD_ROOT/%{destroot}/
chmod -R o+r $RPM_BUILD_ROOT/%{destroot}
find $RPM_BUILD_ROOT%{destroot}/ \
     \( -name .project \
     -o -name .DS_Store \
     -o -name \*.bak \
     -o -name \*-BAK \
     -o -name Thumbs.db \
     -o -name sync-kirayi \) -delete
find $RPM_BUILD_ROOT%{destroot}/ -name CVS -depth -exec rm -rf {} \;
find $RPM_BUILD_ROOT%{destroot}/ -type d -exec chmod o+x {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{destroot}


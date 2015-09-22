Name:           bareos-fuse
Version:        0.1
Release:        1%{?dist}
Summary:        Python module to interact with a Bareos backup system
Group:          Productivity/Archiving/Backup
License:        AGPL-3.0
URL:            https://github.com/joergsteffens/bareos-fuse/
Vendor:         The Bareos Team
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:      noarch
BuildRequires:  rsync
Requires:       python-fuse
Requires:       python-bareos

%description
A python module to interact with a Bareos backup system. Also some tools based on this module.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/bin
rsync usr/bin/. %{buildroot}/usr/bin/.

%check

%files
%defattr(-,root,root,-)
%doc README.md
/usr/bin/*

%changelog

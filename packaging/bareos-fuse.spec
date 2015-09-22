Name:           bareos-fuse
Version:        0.1
Release:        1%{?dist}
Summary:        Display Bareos information as filesystem
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
bareos-fuse allows you to display the information of a Bareos Backup System in your filesystem.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/bin
rsync -av usr/bin/. %{buildroot}/usr/bin/.

%check

%files
%defattr(-,root,root,-)
%doc README.md
/usr/bin/*

%changelog

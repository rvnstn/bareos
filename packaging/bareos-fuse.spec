Name:           bareos-fuse
Version:        0.1
Release:        1%{?dist}
Summary:        Backup Archiving REcovery Open Sourced - FUSE
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
Bareos - Backup Archiving Recovery Open Sourced - FUSE

bareos-fuse allows you to display the information of a Bareos Backup System in your filesystem.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/bin %{buildroot}/etc  %{buildroot}/usr
rsync -av bin/. %{buildroot}/bin/.
rsync -av etc/. %{buildroot}/etc/.
rsync -av usr/. %{buildroot}/usr/.


%check

%files
%defattr(-,root,root,-)
%doc README.md
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/*
/bin/*
/usr/bin/*

%changelog


# OE: conditional switches
#
#(ie. use with rpm --rebuild):
#
#	--with diet	Compile dcetest against dietlibc
#
# 

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary: 	The @stake MSRPC dumper
Name:		dcetest
Version:	2.0
Release:	%mkrel 4
License:	GPL
Group:		Networking/Other
URL:		http://www.atstake.com/research/tools/info_gathering/
Source0:	%{name}.tar.bz2
Patch0:		%{name}-%{version}-optflags.patch
%if %{build_diet}
BuildRequires: dietlibc-devel >= 0.20-1mdk
%endif

%description
This little utility dumps MSRPC endpoint information from Windows 
systems. Similar to the rpcdump program from Microsoft, but does 
not need a DCE stack and so runs on Unixes. dcetest can be very 
useful once inside a DMZ to fingerprint Windows machines on the 
network. dcetest operates over TCP port 135. (Think of it as 
rpcinfo -p against Windows.)

%prep

%setup -q -n %{name}
%patch0 -p0 -b .optflags

%build

%if %{build_diet}
# OE: use the power of dietlibc
make CC="diet gcc -D_BSD_SOURCE -D_GNU_SOURCE -s -static"
%else
%make
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}

install -m755 %{name} %{buildroot}%{_bindir}/%{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG README
%{_bindir}/%{name}



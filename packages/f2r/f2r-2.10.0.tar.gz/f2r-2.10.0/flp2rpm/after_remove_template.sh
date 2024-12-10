#!/bin/bash
versions_installed=$1
profile_file=/etc/profile.d/o2.sh
devel_file=/etc/profile.d/o2-devel.sh
ld_file=/etc/ld.so.conf.d/o2-x86_64.conf

if [ $versions_installed == 0 ]; then
  package=<%= @name %>
  package=${package#"o2-"} #trim o2-prefix
  package_underscore=${package//-/_}

  sed -i "/${package_underscore^^}_ROOT/d" $profile_file
fi

num_installed_packages=$(rpm -qa | grep -c ^o2-)

if [ $num_installed_packages == 1 ]; then
  rm -f $profile_file
  rm -f $ld_file
fi

num_installed_devel=$(rpm -qa | grep -c ^o2-.*-devel)
if [ $num_installed_devel == 1 ]; then
  rm -rf $devel_file
fi

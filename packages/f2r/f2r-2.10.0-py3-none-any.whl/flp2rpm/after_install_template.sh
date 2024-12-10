#!/bin/bash

profile_file=/etc/profile.d/o2.sh
devel_file=/etc/profile.d/o2-devel.sh
ld_file=/etc/ld.so.conf.d/o2-x86_64.conf
package_root=/opt/o2
package=<%= @name %>

if [ ! -f $profile_file ]; then

  echo "export PYTHONPATH=${package_root}/lib:\$PYTHONPATH" >> $profile_file
  echo "export ROOT_DYN_PATH=${package_root}/lib:\$ROOT_DYN_PATH" >> $profile_file
  echo "export ROOT_INCLUDE_PATH=${package_root}/include:\$ROOT_INCLUDE_PATH" >> $profile_file
  echo "export ROOT_INCLUDE_PATH=${package_root}/include/GPU:\$ROOT_INCLUDE_PATH" >> $profile_file
  echo "export ROOT_INCLUDE_PATH=${package_root}/include/fairmq:\$ROOT_INCLUDE_PATH" >> $profile_file
  echo "export ROOT_INCLUDE_PATH=${package_root}/include/QualityControl:\$ROOT_INCLUDE_PATH" >> $profile_file
  echo "export ROOT_INCLUDE_PATH=${package_root}/include/vmc:\$ROOT_INCLUDE_PATH" >> $profile_file
  echo "export PATH=${package_root}/bin:\$PATH" >> $profile_file
  chmod a+x $profile_file
fi;

if ! grep -Fxq "${package_root}/lib" "$ld_file" ; then  echo "${package_root}/lib" >> $ld_file; fi;
if ! grep -Fxq "${package_root}/lib64" "$ld_file" ; then  echo "${package_root}/lib64" >> $ld_file; fi;
/usr/sbin/ldconfig

versions_installed=$1
if [ $versions_installed == 1 ]; then
  package=${package#"o2-"} #trim o2- prefix
  package_underscore=${package//-/_}
  echo "export ${package_underscore^^}_ROOT=${package_root}" >> $profile_file
fi

devel_suffix="devel"
if [[ "$package" == *"$devel_suffix"* ]]; then
  if [ ! -f $devel_file ]; then
    echo "export LIBRARY_PATH=/opt/o2/lib/" >> $devel_file
    echo "export CPLUS_INCLUDE_PATH=/opt/o2/include/" >> $devel_file
    echo "source /opt/rh/gcc-toolset-12/enable" >> $devel_file
    echo "export PATH=${package_root}/bin-safe:\$PATH" >> $devel_file
  fi
fi

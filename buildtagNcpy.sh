#!/bin/sh
###################################################################################################################
### Author: Shivaji Thanneeru
### Date Created:3/26/2015
###################################################################################################################
if [ $# -ne 2 ]
    then echo Usage: `basename $0` tag spec file
    echo Example: `basename $0` RC.01408.001.00.t.2 rp-webapp.spec
    echo ""
else
   hg pull -u
# rpmbuild -bb --target noarch --define 'svn_tag RC.01408.001.00.t.2' rp-webapp.spec
   REGCMND="rpmbuild -bb --target noarch --define 'svn_tag $1' $2 | awk '/Wrote:/ { print \$2 }'"
   GENERATED_RPMS=`eval $REGCMND`
   echo $GENERATED_RPMS
   ISRPM_GENERATED=$?
   if [ $ISRPM_GENERATED == 0 ]
   then
      scp $GENERATED_RPMS rpm_server:/opt/rpms/
      ISCPED=$?
      if [ $ISCPED == 0 ]
      then
         rm $GENERATED_RPMS
      fi
   fi
   for I in $GENERATED_RPMS
   do
      RPM=`echo $I | awk -F"/" '{print $NF}'`
      if [ `echo $RPM | awk '{s=toupper($0)} s~/WEBAPP-STATIC/ {print $0}'` ] || [ `echo $RPM | awk '{s=toupper($0)} s~/PAY/ {print $0}'` ]
        then
        STSTIC_RPM=$RPM
        echo Static RPM : $STSTIC_RPM
      elif [ `echo $RPM | awk '{s=toupper($0)} s~/WEBAPP-APP/ {print $0}'` ]
        then
        WEBAPP_RPM=$RPM
        echo WEBAPP RPM : $WEBAPP_RPM
      elif [ `echo $RPM | awk '{s=toupper($0)} s~/CONF/ {print $0}'` ]
        then
        CONF_RPM=$RPM
        echo CONF RPM : $CONF_RPM
      fi
   done
fi


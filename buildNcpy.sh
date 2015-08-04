#!/bin/sh
###################################################################################################################
### Author: Shivaji Thanneeru
### Date Created:3/26/2015
###################################################################################################################
if [ $# -ne 1 ]
    then echo Usage: `basename $0` spec file
    echo Example: `basename $0` webapp.spec
    echo ""
else
   hg pull -u
  REGCMND="rpmbuild -bb --target noarch $1 | awk '/Wrote:/ { print \$2 }'"
# REGCMND="rpmbuild -bb --target noarch  --define 'dev_mode 1' $1 | awk '/Wrote:/ { print \$2 }'"
   GENERATED_RPMS=`eval $REGCMND`
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


#!/bin/sh
if [ $# -ne 2 ]
    then echo Usage: `basename $0` svn-branches-URL Year
    echo Example: `basename $0` svn://URL 2007
    echo "Then it deletes the branches that are created in 2007."
else
    SVNBRANCH=$1
    YEAROFLASTCOMMIT=$2
    for BRANCH in `svn ls $SVNBRANCH`
    do
      REGCMND="svn info svn://URL/$BRANCH | awk '/Last Changed Date: $YEAROFLASTCOMMIT/ { print \$0 }'"
       LASTCHANGEDDATE=`eval $REGCMND`
      if [ ! -z "$LASTCHANGEDDATE" ]
      then
        echo $LASTCHANGEDDATE on svn://SVNURL/$BRANCH
      fi
    done
fi


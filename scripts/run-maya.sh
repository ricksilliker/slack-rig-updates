#!/bin/bash

export MAYA_MODULE_PATH=${MAYA_MODULE_PATH}

if [[ -z "${MAYA_VERSION}" ]]; then
    export MAYA_VERSION=${DEFAULT_MAYA_VERSION}
else
    echo -e "\n\033[92mUsing Maya ${MAYA_VERSION}...\033[0m"    
fi

echo -e "\n\033[92mStarting Maya now...\033[0m"
/Applications/Autodesk/maya${MAYA_VERSION}/Maya.app/Contents/bin/maya &
exit 0
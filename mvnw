#!/bin/sh
# ----------------------------------------------------------------------------
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# ----------------------------------------------------------------------------

MAVEN_PROJECTBASEDIR=`dirname "$0"`

if [ -z "$MAVEN_PROJECTBASEDIR" ]; then
  echo "Could not locate project root directory."
  exit 1
fi

exec "$MAVEN_PROJECTBASEDIR/.mvn/wrapper/maven-wrapper.jar" "$@"

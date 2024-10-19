@echo off
set MAVEN_PROJECTBASEDIR=%~dp0
if not defined MAVEN_PROJECTBASEDIR (
  echo "Could not locate project root directory."
  exit /b 1
)
java -jar "%MAVEN_PROJECTBASEDIR%.mvn\wrapper\maven-wrapper.jar" %*

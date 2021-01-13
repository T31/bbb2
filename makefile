.PHONY: all test

all:
	javac -d bin -classpath extern/gson-2.8.6.jar src/Bbb2.java src/Api/RawApi.java
	javac -d tst/bin -classpath extern/junit-platform-console-standalone-1.7.0.jar tst/Tests.java

test: all
	java -jar extern/junit-platform-console-standalone-1.7.0.jar --classpath tst/bin --scan-class-path

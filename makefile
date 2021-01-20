.PHONY: all test clean

SRC = src/Bbb2.java\
      src/Api/RawApi.java\
      src/Api/AuthorizeAccountResult.java

TST = tst/Tests.java

all:
	javac -d bin -classpath extern/gson-2.8.6.jar $(SRC)
	javac -d tst/bin -classpath extern/junit-platform-console-standalone-1.7.0.jar $(TST)

test: all
	java -jar extern/junit-platform-console-standalone-1.7.0.jar --classpath tst/bin --scan-class-path --disable-ansi-colors

clean:
	rm -rf bin/*
	rm -rf tst/bin/*

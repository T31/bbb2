.PHONY: all test clean

SRC = src/Bbb2.java\
      src/Api/RawApi.java\
      src/Api/Results/AuthorizeAccountResult.java

TST = tst/Tests.java

all:
	javac -d bin -classpath extern/javax.json/javax.json.jar $(SRC)
	javac -d tst/bin -classpath extern/junit-platform-console-standalone-1.7.0.jar $(TST)

test: all
	java -jar extern/junit-platform-console-standalone-1.7.0.jar --classpath tst/bin --scan-class-path --disable-ansi-colors

clean:
	rm -rf bin/*
	rm -rf tst/bin/*

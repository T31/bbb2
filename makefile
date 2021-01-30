.PHONY: all test clean

SRC = src/bbb2/Bbb2.java\
      src/bbb2/Bbb2Exception.java\
      src/bbb2/ExitCode.java\
      src/bbb2/api/Api.java\
      src/bbb2/api/ApiConnectException.java\
      src/bbb2/api/ApiResponseParseException.java\
      src/bbb2/api/ApiProxy.java\
      src/bbb2/api/results/AuthorizeAccountResult.java\
      src/bbb2/util/http/HttpClientProxy.java\
      src/bbb2/util/http/HttpClientProxyBuilder.java\
      src/bbb2/util/http/HttpException.java\
      src/bbb2/util/http/RealClient.java\
      src/bbb2/util/json/JsonObjectProxy.java\
      src/bbb2/util/json/JsonParseException.java

TST = tst/unit_tests/ApiResultsTests.java\
      tst/unit_tests/ApiProxyTests.java\
      tst/unit_tests/StandardLibTests.java\
      tst/mocks/TestHttpClientProxy.java

JSON_JAR = extern/javax.json/javax.json.jar

JUNIT_JAR = extern/junit-platform-console-standalone-1.7.0.jar

all:
	javac -d bin -classpath $(JSON_JAR) $(SRC)
	javac -d tst/bin -classpath $(JUNIT_JAR):$(JSON_JAR) $(SRC) $(TST)

test: all
	java -jar $(JUNIT_JAR) --classpath tst/bin:bin:$(JSON_JAR) --scan-class-path --disable-ansi-colors

clean:
	rm -rf bin/*
	rm -rf tst/bin/*

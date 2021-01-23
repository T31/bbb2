libjsonp-java
libjsonp-java-doc

Rationalization for using asserts
    If an unrecoverable error that can only be fixed by editing the program's source code occurs, the program should report the error and then halt immediately. In such a case, using an assert statement makes perfect sense.

    Being too assert-happy runs the risk of hand-waving away proper error handling (HURR JUST CRASH THE PROGRAM), but sometimes that's 100% the right decision.

    In conclusion, shut up.

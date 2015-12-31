-module(test).
-export([fac/1]).
-export([print/0]).

fac(0) -> 1;
fac(N) -> N * fac(N-1).

print() -> 
    erlang:get_stacktrace().
    %io:format("The value of Term is: ~p.~n", [Term]).

-module(p_test1). 
-export([loop/0, rpc/2]).

rpc(Pid, Request) ->
    Pid ! {self(), Request}, 
    receive
        Response ->
            Response
    end.
loop() ->
    receive
        {From , {rectangle, Width, Ht}} ->
            From ! Width * Ht,
            io:format("Area of rectangle is ~p~n",[Width * Ht]),
            loop();
        {From, {circle, R}} ->
            From ! io:format("Area of circle is ~p~n", [3.14159 * R * R]),
            io:format("Area of circle is ~p~n", [3.14159 * R * R]),
            loop();
        Other ->
            io:format("I don't know what the area of a ~p is ~n",[Other]),
            loop()
    end.

[range]s[ubstitute]/{pattern}/{string}/[flags] [count] 

substitution flags
- [c] [c] Confirm each substitution. 
- [g] Replace all occurrences in the line. 
- [i] Ignore case for the pattern.

1. :%s/old-text/new-text/g  
2. :s/helo/Hello/gi 
3. :1,10s/I/We/g 
4. :'<,'>s/helo/hello/g
5. :s/helo/hello/g 4
6. :s/<his>/her/g
7. %s/\(good\|nice\)/awesome/g
%s/\(good\|nice\)/awesome/g
8. %s/awesome/wonderful/gc
9. %s/^/\=line(".") . ". "/g

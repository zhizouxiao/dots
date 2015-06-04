require "os"

i = 0
a = 0
before = os.time()
while i<10000000000 do
    i = i + 1
    a = a + i
end


print(os.time()-before)
print(a)

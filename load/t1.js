
i = 0
a = 0
before = Date.now()
while(i<1000000000){
    i = i + 1
    a = a + i
}

console.log(Date.now()-before)
console.log(a)

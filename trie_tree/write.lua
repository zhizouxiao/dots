function serialize (o) 
   if type(o) == "number" then
     io.write(o)
   elseif type(o) == "string" then
     io.write(string.format("%q", o)) 
   elseif type(o) == "table" then
     io.write("{\n")
     for k,v in pairs(o) do
       io.write("  ["); serialize(k); io.write("] = ")
       serialize(v)
       io.write(",")
     end 
     io.write("}\n")
   else
     error("cannot serialize a " .. type(o))
   end 
end

root = {_child={}}

function add_ch(ch, node)
    if node._child[ch] == nil then
        new = {_child={}, value=ch}
        node._child[ch] = new
        return new
    else
        return node._child[ch]
    end
end

function set_end(node)
    add_ch('#', node)
end

function add_word(text)
    node = root
    for ch in text:gfind("[%z\1-\127\194-\244][\128-\191]*") do
        node = add_ch(ch, node)
    end
    
    set_end(node)
end


fr = io.open('mgc.config', 'r')
io.input(fr)
line = 'line'
while line do
    line = io.read("*line")
    if line==nil then break end
    add_word(line)
end
fw = io.open('mgc.lua', 'w')

io.output(fw)
io.write("root=")
io.write(serialize(root))
fw.close()

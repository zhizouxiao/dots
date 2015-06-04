require("mgc")

function add_ch(ch, node)
    if node._child[ch] == nil then
        new = {_child={}}
        node._child[ch] = new
        --print("add_ch", ch)
        return node
    else
        return node._child[ch]
    end
end

function is_end(n, node)
    if node._child[n] ~= nil then
        return false
    end
    if node._child['#'] ~=nil then
        return true
    end
    return false
end

function get_child(ch, node)
    return node._child[ch]
end

function replace_bad_word(text, mark)
    --replace bad word with mark
    i = offset
    li = {}
    
    --convert text to table
    n = 0
    for ch in text:gfind("[%z\1-\127\194-\244][\128-\191]*") do
        li[n] = ch
        n = n + 1
    end

    --iterate table
    for k=0, #li do 
        ch = li[k]
        --print(k, ch)
        node = root
        index = k
        node = get_child(ch, node)

        while node do
            n = li[k+1]
            if is_end(n, node) then
                for m=k, index do
                    li[m] = mark
                end
                break
            end
            index = index + 1
            node = get_child(li[index], node)
        end
    end
    --link table to string
    final = ''
    for k=0, #li do
        ch = li[k]
        final = final..ch
    end
    return final
end

function get_bad_word(text)
    --get bad word index, if not return -1
    li = {}
    
    --convert text to table
    n = 0
    for ch in text:gfind("[%z\1-\127\194-\244][\128-\191]*") do
        li[n] = ch
        n = n + 1
    end

    --iterate table
    for k=0, #li do 
        ch = li[k]
        --print(k, ch)
        node = root
        index = k
        node = get_child(ch, node)

        while node do
            n = li[k+1]
            if is_end(n, node) then
                return k
            end
            index = index + 1
            node = get_child(li[index], node)
        end
    end
    return -1
end


--str = "毛泽东,邓小平, a, b, c , 客服, a, fuck, mm, 遊戲管理遊戲管理者|管理員|新手指導員|新手輔導員"
--final = get_bad_word(str)
--print(final)



--str = "我喜欢毛泽东,邓小平, a, b, c , 客服, a, fuck, mm, 遊戲管理遊戲管理者|管理員|新手指導員|新手輔導員"
--final = replace_bad_word(str,'*')
--print(final)



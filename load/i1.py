import lupa
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)

print lua.eval('1+1')

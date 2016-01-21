1. Move curse word-by-word in insert mode: 
- Shift - <Right Arrow> 
- Shift - <Left Arrow> 

2. jump list.
- `:jumps` show jump list.
- `Ctrl-O` jump back to previous spot
- `Ctrl-I` jump forward to next spot

3. Navigate Within a Very Long Line.
- `gj` scroll down a visual line.
- `gk` scroll up a visual line.
- `g^` go to the starting of current visual line
- `g$` go to the end of current visual line
- `gm` go to the middle of current visual line

4. create bookmarks.
- `ma` create a bookmark named **a**.
- `\`a` access the bookmark named a.
- `\`.` access the exact location where the last change was changed.

5. change text
- `s` delete current character & insert mode.
- `S` delete current line & insert mode.
- `4s` delete 4 characters & insert mode.
- `4S` delete 4 characters & insert mode.
- `cc` == `S`
- `C` delete current line from cursor position & insert mode.

6. yank
- `y<char navigation keys>`
- `y<word navigation keys>`
- `y<line navigation keys>`
- `y<mark name>`

7. paste
- `p` after the cursor
- `P` before the cursor
- `"0p` paste last copy

8. Editing with :g
- `:g/^$/d` delete all empty lines
- :g/^\s*$/d delete all empty lines and blank lines
- :g/^$/,/./-j delete 
- :g/pattern/ . w>>filename Extract lines with specific pattern and write it into another file
- :g!/Sales/d v/Sales/d Delete all lines except Sales

9. To execute single Vim command in insert mode.
- `Ctrl-O`

10. view the detail of current file.
- `Ctrl-G`

11. Execute any Vim Command when opening a file
- vim -c '<command 1>' -c '<command 2>' <filename>

12. tabe
- vim -p file1 file2 file3
- `:tabe FILENAME` open in new.
- 
- gt | :tabn     go to next tab
- gT | :tabp    go to previous tab
- {i}gt | :tabn {i}  go to tab in position i
- :tabclose | :tabc 

13. undo & redo
- u single undo
- U undo all latest changes (in the current line)
- Ctrl-R | :red redo

14. open file whose name is under the cursor
- gf open the file in the same window.
- Ctrl-w f open the file in the new window.
- Ctrl-w gf open the file in the new tab

note: gf can open header in c/cpp.

15. vimdiff go to next change [c ]c

16. map 
- :map :write :!cc % && ./a.out
- :map – Vim command to create the map
- :write – Name of the map (map-name)
- :!cc % & ./a.out – The command that should be executed when the map-name is called.

17. Most recent yank (copy) is stored in register 0
Most recent deletion is stored in register 1

18. ; Repeat latest f, F, t or T in forward direction
, ￼Repeat latest f, F, t or T in backward direction

19. :match ErrorMsg /Error/
- :match – the match command
- ErrorMsg – Predefined color scheme (red) available in the Vim. ErrorMsg/WarningMsg/ModeMsg/MoreMsg
- /Error/ - search pattern defined by user

20. Format a paragraph
- gqap

21. Add a bullet point style to List of Items

- Ctrl-V
- Select the first character
- I
- TAB
- *
- ESC ESC
    * a
    * b
    * c

22. Identify the changes done to a file
- :changes

23. refresh screen
- Ctrl-L
24. insert no keyboard characters
- :digraphs
- Ctrl-K {char1} {char2}

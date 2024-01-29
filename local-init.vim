"source $VIMRUNTIME/defaults.vim
if has('win32') || has('win64')
    execute 'source ~/AppData/Local/nvim/init.vim'
else
    execute 'source ~/.config/nvim/init.vim'
endif

" open config files
e ~/.config/nvim/init.vim 
vnew local-init.vim

" open current project files
tabe temp.txt
vnew day17/day17-1.py

" macros
let @d = "GV/DELETE BELOW THIS LINE\<CR>jx\<ESC>"
let @c = "^i# \<ESC>"
let @u = "V/^# \<CR>x\<ESC>"

let g:ale_fixers = {
\	'python': ['black']
\}
"source $VIMRUNTIME/defaults.vim
if has('win32') || has('win64')
    execute 'source ~/AppData/Local/nvim/init.vim'
else
    execute 'source ~/.config/nvim/init.vim'
endif

" open config files
if has('win32') || has('win64')
    e ~/AppData/Local/nvim/init.vim
    vnew ~/AppData/Local/nvim/ginit.vim
else
    e ~/.config/nvim/init.vim 
endif
vnew local-init.vim

" macros
let @d = "GV/DELETE BELOW THIS LINE\<CR>jxo\<ESC>"
let @m = "@d/RUN THIS\<CR>jVy/DELETE BELOW THIS LINE\<CR>:\<C-R>\"\<CR>"
let @c = "^i# \<ESC>"
let @u = "V:s/^# //g\<CR>"

let g:ale_fixers = {
\	'python': ['black']
\}

" open current project files
tabe temp.txt
vnew day19/day19-2.py

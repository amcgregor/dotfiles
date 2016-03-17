" Alice's ordinarily complicated Vim configuration.
" Feel free to ridicule whatever you may in here.
"
" Remember to run `git submodule init` and `git submodule update` prior to use.
"

" Configuration {{{

let g:alice_width = 120	" Marrow:OSC standardizes on 120 columns.
let g:alice_tabs = 1	" Save the planet; use tabs. Set to zero to use heathen spaces.
let g:alice_tabsize = 4	" Default tab size.

" }}}
"
" Below here there be dragons.
"

" Pathogen Module Loading {{{

filetype off
execute pathogen#infect()
execute pathogen#helptags()
filetype on

" }}}

" Colors {{{

set background=dark
colorscheme apprentice

" TODO: Find a scheme less offensive on limited terminals that's still pretty in high-color.

syntax enable	" Enable syntax highlight processing.

" }}}

" Spaces & Tabs {{{
" We prefer tabs, but this should depend on the configuration directive. TODO

set tabstop=4	" Number of spaces to use as tab width.
set noexpandtab	" We have no desire to turn these into spaces.
set shiftwidth=4
set modelines=1
filetype indent on
filetype plugin on
set autoindent
set backspace=indent,eol,start

" }}}

" Basic User Interface {{{

set number	" Show line numbers.
set cursorline	" Highlight the currently selected line.
set list listchars=tab:⇥⋅,trail:⋅,nbsp:⋅	" Show invisibles.
filetype indent on	" Load per-filetype indentation rules from ~/.vim/indent/<type>.vim
" set lazyredraw	" Bypass screen updates mid-macro.
set ttyfast	" Faster redraw for modern terminals.
set showmatch	" Highlight matching brackets when selected.
set laststatus=2	" Always show file status line.

set omnifunc=syntaxcomplete#Complete

" }}}

" Searching {{{

set incsearch	" Search as you type.
set hlsearch	" Highlight search matches.
set ignorecase	" Ignore case when searching.

" Shortcut for hiding search history: ,<space>
nnoremap <leader><space> :nohlsearch<CR>

" }}}

" Code Folding {{{

set foldenable	" Enable code folding by default.
set foldlevelstart=1	" One level by default; module-scope classes and functions.
set foldnestmax=10	" A sane maximum number of recursive folds.

" Open and close a fold using the spacebar.
nnoremap <space> za

set foldmethod=indent	" Fold on indentation level, which works for Python.

" }}}

" Movement {{{

" Move through visually soft wrapped lines.
nnoremap j gj
nnoremap k gk

" Beginning and end of line.
nnoremap B ^
nnoremap E $

" Unbind the previously mentioned $ and ^ keys.
nnoremap $ <nop>
nnoremap ^ <nop>

" Highlight last inserted text.
nnoremap gV `[v`]

" }}}

" Leader Shortcuts {{{

let mapleader=","	" Leader is comma.

" Toggle gundo (better undo).
nnoremap <leader>u :GundoToggle<CR>

" Toggle the NERDTree.
nnoremap <leader>f :NERDTreeToggle<CR>

" Save the current session (re-open with: vim -S).
nnoremap <leader>s :mksession<CR>

" Rapidly search using ag.vim (ag command-line tool, like ack).
nnoremap <leader>a :Ag

" Toggle line number style.
nnoremap <leader>l :call ToggleNumber()<CR>

" Symbol list toggle.
nnoremap <leader>o :TlistToggle<CR>

" }}}

" CtrlP (Fuzzy File Search) Settings {{{

let g:ctrlp_match_window = 'bottom,order:ttb'
let g:ctrlp_switch_buffer = 0
let g:ctrlp_working_path_mode = 0
" let g:ctrlp_user_command = 'ag %ks -l --nocolor --hidden -g ""'
let g:ctrlp_user_command = ['.git', 'cd %s && git ls-files -co --exclude-standard']

set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*~
let g:ctrlp_custom_ignore = '\v[\/]\.(git|hg|svn)$'

" }}}

" Language-Specific Settings {{{

augroup configgroup
	autocmd!
	autocmd VimEnter * highlight clear SignColumn
	autocmd FileType python setlocal commentstring=#\ %s
	autocmd FileType python setlocal tabstop=4
augroup END

" }}}

" Powerline / Airline Settings {{{

let g:airline#extensions#tabline#enabled = 1	" Enable top open buffer list.

" Disable fancy tabs.
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''

let g:airline#extensions#branch#format = 'Git_flow_branch_format'
let g:git_flow_prefixes = {
	\ 'master': '',
	\ 'develop': '',
	\ 'feature': 'f/',
	\ 'release': 'r/',
	\ 'hotfix': 'h/',
	\ 'support': 's/',
	\ 'versiontag': 'v/'
\ }

" }}}

" Custom Functions {{{

" Toggle between orderly line numbers and relative line numbers.
function! ToggleNumber()
	if(&relativenumber == 1)
		set norelativenumber
		set number
	else
		set relativenumber
	endif
endfunc

" }}}

" NERDTree Settings {{{

let NERDTreeChDirMode=2
let NERDTreeIgnore=['\.vim$', '\~$', '\.pyc$', '\.swp$', '\.egg-info$']
let NERDTreeSortOrder=['^__\.py$', '\/$', '*', '\.swp$',  '\~$']
let NERDTreeShowBookmarks=1
let NERDTreeQuitOnOpen=1
let NERDTreeMouseMode=2

" }}}

" Syntastic {{{

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_aggregate_errors = 1
let g:syntastic_python_python_use_codec = 1
let g:syntastic_python_python_exec = '/usr/bin/env python'
let g:syntastic_python_checkers = ['python', 'frosted']

" }}}

" Backup Configuration {{{

set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set backupskip=/tmp/*,/private/tmp/*
set directory=~/.vim-tmp,~/.tmp,~tmp,/var/tmp,/tmp
set writebackup

" }}}

" Python "Mode" Configuration {{{

let g:pymode = 1
let g:pymode_doc = 1	" Show docstring for selected completion.
let g:pymode_doc_bind = 'K'
let g:pymode_folding = 1
let g:pymode_indent = 0
let g:pymode_quickfix_minheight = 0
let g:pymode_trim_whitespaces = 0
let g:pymode_options = 0
let g:pymode_options_max_line_length = 119
" let g:pymode_python = 'python3'
let g:pymode_rope_lookup_project = 1
let g:pymode_rope_autoimport = 1
let g:pymode_lint_ignore = 'W191,W293,E251,W391'

set tags=tags;$HOME/.vim/tags/

let Tlist_Ctags_Cmd='/usr/local/bin/ctags'
let Tlist_GainFocus_On_ToggleOpen = 1
let Tlist_Close_On_Select = 1
let Tlist_Use_Right_Window = 1
let Tlist_File_Fold_Auto_Close = 1

" }}}

" vim:foldmethod=marker:foldlevel=0

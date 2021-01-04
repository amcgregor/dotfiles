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
nnoremap <home> $

" Unbind the previously mentioned $ and ^ keys.
nnoremap $ <nop>
nnoremap ^ <nop>

" Highlight last inserted text.
nnoremap gV `[v`]

" Do not automatically clean indentation when moving away from the line.
:set cpoptions+=I

" Ensure we always have some visible context.
set scrolloff=6

" }}}

" Leader Shortcuts {{{

nnoremap G :G

let mapleader=","	" Leader is comma.

" Toggle the NERDTree.
nnoremap <silent> <leader>f :NERDTreeToggle<CR>
nnoremap <silent> <leader>v :NERDTreeFind<CR>

" Enable git blame status line reporting.
nnoremap <Leader>s :<C-u>call gitblame#echo()<CR>

" Rapidly search using ag.vim (ag command-line tool, like ack).
nnoremap <leader>a :Ag 
let g:ag_highlight=1

" Toggle line number style.
nnoremap <leader>l :call ToggleNumber()<CR>

" Symbol list toggle.
nnoremap <leader>B :TagbarToggle<CR>

" Allow for quick hiding of the active search.
nnoremap <leader><space> :noh<CR>

" Toggle coverage gutter colouring.
nnoremap <leader>c :Coveragepy report<CR>
nnoremap <leader>m :Coveragepy show<CR>

" Pytest execution.
nnoremap <leader>t :Pytest file<CR>
nnoremap <leader>T :Pytest project<CR>
nnoremap <leader>M :Pytest method<CR>

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

let g:xml_syntax_folding = 0
set linebreak
set breakindent

augroup configgroup
	autocmd!
	autocmd VimEnter * highlight clear SignColumn
	autocmd FileType python setlocal commentstring=#\ %s
	autocmd FileType python setlocal tabstop=4
	autocmd FileType python setlocal noexpandtab
	autocmd FileType python setlocal shiftwidth=4
	autocmd FileType python setlocal breakindentopt=shift:8
augroup END

" }}}

" Path Mapping Configuration {{{

let g:env_mappings = {'HOME': '~', 'VIRTUALENV': '↬'}

" }}}

" Airline Settings {{{

let g:airline_theme = 'bubblegum'

let g:airline#extensions#tabline#enabled = 1	" Enable top open buffer list.
let g:airline#extensions#tabline#buffers_label = 'BUF'
let g:airline#extensions#tabline#tabs_label = 'TAB'

" Disable fancy tabs.
let g:airline_powerline_fonts = 1

let g:airline#extensions#branch#format = 2

let g:airline#extensions#hunks#hunk_symbols = ['+', '±', '−']

let g:airline#extensions#whitespace#mixed_indent_algo = 2
let g:airline#extensions#whitespace#checks = [ 'indent', 'long', 'mixed-indent-file' ]

let g:airline#extensions#tabline#buffer_idx_mode = 1
nmap <leader>1 <Plug>AirlineSelectTab1
nmap <leader>2 <Plug>AirlineSelectTab2
nmap <leader>3 <Plug>AirlineSelectTab3
nmap <leader>4 <Plug>AirlineSelectTab4
nmap <leader>5 <Plug>AirlineSelectTab5
nmap <leader>6 <Plug>AirlineSelectTab6
nmap <leader>7 <Plug>AirlineSelectTab7
nmap <leader>8 <Plug>AirlineSelectTab8
nmap <leader>9 <Plug>AirlineSelectTab9
nmap <leader>- <Plug>AirlineSelectPrevTab
nmap <leader>= <Plug>AirlineSelectNextTab

" let g:airline#extensions#tabline#formatter = 'alice'

let g:airline#extensions#promptline#snapshot_file = "~/.shell_prompt.sh"
let g:airline#extensions#promptline#enabled = 0
" let g:airline#extensions#promptline#color_template = 'normal' (default)
" let g:airline#extensions#promptline#color_template = 'insert'
" let g:airline#extensions#promptline#color_template = 'visual'
let g:airline#extensions#promptline#color_template = 'replace'

let g:promptline_theme = 'airline'
"		\'a': [fg, bg, attr],
"		\'b': [fg, bg, attr],
"		\'c': [fg, bg, attr],
"		\'x': [fg, bg, attr],
"		\'y': [fg, bg, attr],
"		\'z': [fg, bg, attr],
"		\'warn': [fg, bg, attr]}

let g:promptline_preset = {
		\'a': [ '$(basename $VIRTUAL_ENV 2>/dev/null)' ],
		\'b': [ promptline#slices#cwd() ],
		\'y': [ promptline#slices#git_status(), '$(git rev-parse --short HEAD 2>/dev/null)' ],
		\'z': [ promptline#slices#vcs_branch() ],
		\'warn' : [ promptline#slices#last_exit_code(), promptline#slices#jobs() ]}

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
let NERDTreeIgnore=['\.vim$', '\~$', '\.pyc$', '\.swp$', '\.egg-info$', '__pycache__', 'coverage.xml']
let NERDTreeSortOrder=['^__\.py$', '\/$', '*', '\.swp$',  '\~$']
let NERDTreeShowBookmarks=1
let NERDTreeQuitOnOpen=1
let NERDTreeMouseMode=2
let NERDTreeSortHiddenFirst=1
let NERDTreeQuitOnOpen = 1
let NERDTreeAutoDeleteBuffer = 1
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1

autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

let g:NERDTreeGitStatusIndicatorMapCustom = {
    \ "Modified"  : "✹",
    \ "Staged"    : "✚",
    \ "Untracked" : "✭",
    \ "Renamed"   : "➜",
    \ "Unmerged"  : "═",
    \ "Deleted"   : "✖",
    \ "Dirty"     : "✗",
    \ "Clean"     : "✔︎",
    \ 'Ignored'   : '☒',
    \ "Unknown"   : "?"
    \ }

" f459
" 

" }}}

" Syntastic {{{

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_aggregate_errors = 1
let g:syntastic_python_python_use_codec = 1
let g:syntastic_python_python_exec = '/usr/bin/env python3.8'
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

let g:pymode = 1  " Enable Pymode generally.
let g:pymode_python = 'python3.8'
let g:pymode_run_key = '<leader>r'  " Execute the script by pressing ',r'
let g:pymode_lint_checkers = ['pyflakes', 'mccabe']
let g:pymode_lint_ignore = 'W191,W293,E251,W391'
let g:pymode_lint_on_fly = 0
let g:pymode_lint_unmodified = 0
let g:pymode_lint_write = 0
let g:pymode_breakpoint = 0
let g:pymode_quickfix_minheight = 1
let g:pymode_quickfix_maxheight = 5
let g:pymode_rope_autoimport = 1
let g:pymode_rope_autoimport_generate = 0
let g:pymode_rope_lookup_project = 1
let g:pymode_rope_goto_definition_bind = '<leader>g'	" 'Go to definition' by pressing ',g'
let g:pymode_rope_goto_definition_cmd = 'e'	" Jump to editing the file.
let g:pymode_doc_bind = '<leader>k'	" Browse the documentation by pressing ',k'
let g:pymode_folding = 1	" Allow fancy folding.
let g:pymode_indent = 0	" Disable the default (space-based) indentation rules.
let g:pymode_quickfix_minheight = 0	" Minimum height is invisible.
let g:pymode_trim_whitespaces = 0	"We have our own whitespace policy.
let g:pymode_options = 0
let g:pymode_options_max_line_length = 119
let g:pymode_rope_rename_bind = '<leader>R'
let g:pymode_rope_complete_on_dot = 0
let g:pymode_virtualenv = 1
let g:pymode_virtualenv_path = '/Users/amcgregor/Projects/marrow/.venv'

set tags=tags;$HOME/.vim/tags/

let Tlist_Ctags_Cmd='/usr/local/bin/ctags'
let Tlist_GainFocus_On_ToggleOpen = 1
let Tlist_Close_On_Select = 1
let Tlist_Use_Right_Window = 1
let Tlist_File_Fold_Auto_Close = 1

if has('gui_macvim')
	" set pythonthreehome="/usr/local/Cellar/python3/3.6/Frameworks/Python.framework/Versions/3.6"
	" set pythonthreedll=/usr/local/Cellar/python3/3.6.0/Frameworks/Python.framework/Versions/3.6/lib/libpython3.6m.dylib
endif

let $VIRTUAL_ENV="/Users/amcgregor/Projects/marrow/.venv"
" let $PATH="/Users/amcgregor/Projects/marrow/.venv/bin:$PATH"

" }}}

" Kite Integration {{{
let g:kite_auto_complete=0
let g:kite_snippets=0
let g:kite_tab_complete=1
let g:kite_documentation_continual=1
" }}}

" vim:foldmethod=marker:foldlevel=0

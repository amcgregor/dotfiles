" Vim syntax file
" Language:	Mako HTML template
" Maintainer:	David Vincelli <david@register.ca>
" Last Change:	2011 Apr 29

" Shamelessly taken from Armin Ronacher's htmljinja.vim

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

if !exists("main_syntax")
  let main_syntax = 'html'
endif

if version < 600
  so <sfile>:p:h/mako.vim
  so <sfile>:p:h/html.vim
else
  runtime! syntax/mako.vim
  runtime! syntax/html.vim
  unlet b:current_syntax
endif

let b:current_syntax = "htmlmako"

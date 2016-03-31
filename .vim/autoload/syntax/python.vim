" Thanks to ntnn in #vim on Freenode IRC!

let g:fold_space = '\v^\s*'

let s:fold_decorator = g:fold_space . '\@'
let s:fold_class_or_def = g:fold_space . '(class |def )'
let s:fold_return = g:fold_space . 'return'
let s:fold_docstring_oneline = g:fold_space . '""".*"""'
let s:fold_docstring_start = g:fold_space . '"""[[:alnum:]]*'
let s:fold_docstring_end = g:fold_space . '"""$'

fu! python#FoldExpr()
    let pl = getline(v:lnum - 1)
    let plind = indent(v:lnum - 1)
    let l = getline(v:lnum)
    let lind = indent(v:lnum)
    let nl = getline(v:lnum +  1)
    let nlind = indent(v:lnum + 1)

    if v:lnum == 1
        return '1>'
    endif

    if l =~ s:fold_return
        return 's1'
    endif

    if l =~ s:fold_empty
        if pl =~ s:fold_empty
            return '<1'
        elseif nl =~ s:fold_empty
            return '='
        elseif plind > nlind && (nl =~ s:fold_decorator || nl =~ s:fold_class_or_def)
            return "s1"
        endif
    endif

    if l =~ s:fold_decorator || l =~ s:fold_class_or_def
        if pl =~ s:fold_decorator || plind > lind
            return '='
        endif
        return "a1"
    endif

    if l =~ s:fold_docstring_oneline
        return '='
    endif

    if l =~ s:fold_docstring_end
        return 's1'
    endif
    if l =~ s:fold_docstring_start
        return 'a1'
    endif

    return '='
endfu

fu! python#FoldText()
    let l = v:foldstart
    while getline(l) !~ s:fold_class_or_def && l != v:foldend
        let l = l + 1
    endwhile
    if l == v:foldend
        let l = v:foldstart
    endif
    return getline(l)
endfu

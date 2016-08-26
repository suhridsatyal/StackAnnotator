set t_Co=256
if &term =~ '256color'
  " disable Background Color Erase (BCE) so that color schemes
  " render properly when inside 256-color tmux and GNU screen.
  " see also http://snk.tuxfamily.org/log/vim-256color-bce.html
  set t_ut=
endif

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
syntax on
filetype plugin indent on
set nu "Set line number
" Ignore compiled files
set wildignore=*.o,*~,*.pyc
" Highlight search results
set hlsearch
" Ignore case when searching
set ignorecase
" Incremental search
set incsearch
" When searching try to be smart about cases
set smartcase
" Show matching brackets when text indicator is over them
set showmatch
"Save buffer automatically when changing files
set autowrite
"Always reload buffer when external changes detected
set autoread
" this enables "visual" wrapping
set wrap
" this turns off physical line wrapping (ie: automatic insertion of newlines)
set textwidth=0 wrapmargin=0

" ignore these files when completing names and in Ex
set wildignore=.svn,CVS,.git,*.o,*.a,*.class,*.mo,*.la,*.so,*.obj,*.swp,*.jpg,*.png,*.xpm,*.gif,*.pdf,*.bak,*.beam,*.dvi
" set of file name suffixes that will be given a lower priority when it comes to matching wildcards
set suffixes+=.old

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Text, tab and indent related
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab
" Text wrapping
" set lbr
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Files, backups and undo
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Turn backup off, since most stuff is in SVN, git et.c anyway...
set nobackup
set nowb
set noswapfile
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Font
set background=dark
hi Special guifg=#799d6a
" colorscheme solarized
"dark: twilight, candycode, camo, gentooish, jellybeans, rainbow_neon
"dark: railscasts, rootwater, rdark, slate, symfony, watermark, wombat
"dark: zenburn, pacific, chlordane, greenvision, darkspectrum
"light: dawn, tidy, eclipse, python, louver, pleasant, tango-morning
"light: google, professional, khaki, habiLight, ashen, automation
"
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Tabs and splits
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Tabs
nnoremap <A-h> :tabprevious<CR>
nnoremap <A-l> :tabnext<CR>
nnoremap <silent> <leader> <A-h> :execute 'silent! tabmove ' . (tabpagenr()-2)<CR>
nnoremap <silent> <leader> <A-l> :execute 'silent! tabmove ' . tabpagenr()<CR>

"Splits
" easier navigation between split windows
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-h> <C-w>h
nnoremap <C-l> <C-w>l

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Moving around
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Treat long lines as break lines (useful when moving around in them)
map j gj
map k gk

" Use shift-H and shift-L for move to beginning/end
nnoremap H 0
nnoremap L $

" Return to last edit position when opening files (You want this!)
autocmd BufReadPost *
     \ if line("'\"") > 0 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Custom mappings (editing)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Use \d to delete without adding it to the yanked stack (also, in visual mode)
nnoremap <silent> <leader>d "_d
vnoremap <silent> <leader>d "_d

" Quick yanking to the end of the line
nnoremap Y y$

" Yank/paste to the OS clipboard with \y and \p
nnoremap <leader>y "+y
nnoremap <leader>Y "+yy
nnoremap <leader>p "+p
nnoremap <leader>P "+P

" disable search highlight temporarily
nnoremap <silent> <leader>h :<C-u>nohlsearch<CR><C-l>

"Remove trailing whitespace
nnoremap <silent> <leader>1 :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar>:nohl<CR>
"Remove leading whitespace
nnoremap <silent> <leader>2 :le<CR>

" Use space to jump down a page (like browsers do)...
nnoremap <Space> <PageDown>

" Insert cut marks...
nmap -- A<CR><CR><CR><ESC>k6i-----cut-----<ESC><CR>

"Swap : with ;
nnoremap ; :

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Util
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Auto refresh .vimrc
autocmd! bufwritepost .vimrc source %

" Quickly edit/reload the vimrc file
nmap <silent> <leader>1` :e $MYVIMRC<CR>
nmap <silent> <leader>` :so $MYVIMRC<CR>

" Map fullscreen shortcut
map <silent> <F11>
\    :call system("wmctrl -ir " . v:windowid . " -b toggle,fullscreen")<CR>

" Command aliases
cnoreabbrev <expr> W ((getcmdtype() is# ':' && getcmdline() is# 'W')?('w'):('W'))
cnoreabbrev <expr> Wq ((getcmdtype() is# ':' && getcmdline() is# 'Wq')?('wq'):('Wq'))
cnoreabbrev <expr> WQ ((getcmdtype() is# ':' && getcmdline() is#'WQ')?('wq'):('WQ'))
cnoreabbrev <expr> Q ((getcmdtype() is# ':' && getcmdline() is# 'Q')?('q'):('Q'))
cnoreabbrev <expr> Qa ((getcmdtype() is# ':' && getcmdline() is#'Qa')?('qa'):('Qa'))
cnoreabbrev <expr> QA ((getcmdtype() is# ':' && getcmdline() is#'QA')?('qa'):('QA'))
" Command alias for saving and closing without permission
cnoreabbrev <expr> ww ((getcmdtype() is# ':' && getcmdline() is# 'ww')?('w !sudo tee % > /dev/null %'):('ww'))
cnoreabbrev <expr> qq ((getcmdtype() is# ':' && getcmdline() is# 'qq')?('q!'):('qq'))

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Cool Stuff
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Make the 80th column stand out
highlight ColorColumn ctermbg=magenta
call matchadd('ColorColumn', '\%80v', 100)

" Toggle visibility of naughty characters
" Make naughty characters visible...
" (uBB is right double angle, uB7 is middle dot)
exec "set lcs=tab:\uBB\uBB,trail:\uB7,nbsp:~"

augroup VisibleNaughtiness
    autocmd!
    autocmd BufEnter * set list
    autocmd BufEnter *.txt set nolist
    autocmd BufEnter *.vp* set nolist
    autocmd BufEnter * if !&modifiable
    autocmd BufEnter * set nolist
    autocmd BufEnter * endif
augroup END
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Visual mode stuff
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Search in visual mode
xnoremap * :<C-u>call <SID>VSetSearch()<CR>/<C-R>=@/<CR><CR>
xnoremap # :<C-u>call <SID>VSetSearch()<CR>?<C-R>=@/<CR><CR>

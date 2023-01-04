"-----------------------------------------------------------------------------
" Jakob Janzen
" jakob.janzen80@gmail.com
" 2022-12-18
"-----------------------------------------------------------------------------

"[ GENERAL ]
syntax on

if has('nvim')
  """ Neovim specific commands.
else
  """ Vim specific commands.
  set nocompatible
  " Color support.
  set t_Co=256 t_ti= t_te= t_vb=
endif

" Encoding.
if has("multi_byte")
  set encoding=utf-8
  set fileencoding=utf-8
  set termencoding=utf-8
endif
" File management.
set nobackup nowritebackup noswapfile
set shortmess+=I history=1000
filetype plugin indent on
set autochdir autoread autowrite
set hidden bufhidden=hide clipboard=unnamed

"[ AUTO COMMANDS ]
augroup MakeFile
  autocmd!
  autocmd FileType make setlocal noexpandtab
augroup END
augroup CMake
  autocmd!
  autocmd BufRead,BufNewFile *.cmake,CMakeLists.txt,*.cmake.in setfiletype cmake
  autocmd BufRead,BufNewFile *.ctest,*.ctest.in setfiletype cmake
augroup END
augroup C_Cpp
  autocmd!
  autocmd FileType c,cpp setlocal comments-=:// comments+=f://
augroup END
augroup Python
  autocmd!
  autocmd FileType python setlocal tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab
augroup END

"[ LANGUAGE EXTRA ]
let g:is_bash=1
let g:sh_fold_enabled=7
"let g:sh_no_error= 1
"let readline_has_bash=1

"[ KEY MAPPING ]
let mapleader=","
" Clear highlighted search results.
nnoremap <LEADER>c :let @/ = ""<CR>
" Toggle highlighted search results.
nnoremap <LEADER>h :set hlsearch!<CR>
" Toggle numbers.
nnoremap <LEADER>n :set number!<CR>
" Highlight trailing spaces.
nnoremap <LEADER>t :/\s\+$<CR>
" Avoid finger dislocations on german keyboards.
nnoremap k gk
nnoremap j gj
nnoremap B ^
nnoremap E $
nnoremap $ <NOP>
nnoremap ^ <NOP>
" Disable arrow-keys for moving.
nnoremap <LEFT> <NOP>
nnoremap <RIGHT> <NOP>
nnoremap <DOWN> <NOP>
nnoremap <UP> <NOP>
" Fast window moving.
nnoremap <C-H> <C-W>h
nnoremap <C-L> <C-W>l
nnoremap <C-J> <C-W>j
nnoremap <C-K> <C-W>k
" Fast window resizing.
nnoremap <S-H> :vertical resize -2<CR>
nnoremap <S-L> :vertical resize +2<CR>
nnoremap <S-J> :resize -2<CR>
nnoremap <S-K> :resize +2<CR>
" Fast buffers and tabs navigation.
nnoremap <C-DOWN> :bprevious<CR>
nnoremap <C-UP> :bnext<CR>
nnoremap <C-LEFT> :tabprevious<CR>
nnoremap <C-RIGHT> :tabnext<CR>
" Umlaute (German keyboard compatibility).
map! ä <Char-228>
map! Ä <Char-196>
map! ö <Char-246>
map! Ö <Char-214>
map! ü <Char-252>
map! Ü <Char-220>
map! ß <Char-223>

"[ COLOR ]
highlight clear
set background=dark
colorscheme default
let &colorcolumn="80,100,120"
highlight ColorColumn cterm=Reverse

"[ INTERFACE ]
set mouse=a
set mousefocus nomousehide
set laststatus=2 showcmd showmode
set cmdheight=1 confirm
set wildmenu wildmode=longest,list:longest wildignorecase wildignore=*.o,*~,*.pyc
set noerrorbells novisualbell timeoutlen=500
set statusline=
set statusline+=%f%m%r%h%w[%{&ff}][%Y]
set statusline+=\ %=[\%03.3b][0x\%03.3B]
set statusline+=\ [%05l,%05v][%p%%][%05L]
" Ensure correct displaying of the interface.
redrawstatus!
redraw!

"[ EDITOR ]
" Indentation and tabs.
set autoindent smartindent cindent smarttab expandtab
set tabstop=2 softtabstop=2 shiftwidth=2 shiftround
set linebreak backspace=indent,eol,start
" Folding.
set foldcolumn=1 foldenable foldmethod=indent foldnestmax=3 foldlevel=9
" Searching.
set incsearch ignorecase smartcase hlsearch
set wrapscan magic gdefault
" Completion.
set completeopt=menuone,menu,longest,preview
set formatoptions-=cro
" Clear highlighted search results.
let @/ = ""


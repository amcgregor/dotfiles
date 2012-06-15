# Alice's over-engineered z-shell configuration, released in the public domain.
# Private and publicly exported variables.

# Alert me when other users log in.
watch=(notme)

DIRSTACKSIZE=20
LISTPROMPT=''
LOGCHECK=60
REPORTTIME=2
SPROMPT='zsh: correct '%R' to '%r' ? ([Y]es/[N]o/[E]dit/[A]bort) '
WATCHFMT='%n %a %l from %m at %t.'

export BROWSER='open'
export CLICOLOR=1 LSCOLORS="ExGxFxDxCxDxDxhbhdacEc"
export EDITOR='choc -w'
export LESSOPEN="|lesspipe.sh %s"
export VISUAL=$EDITOR

# export LS_COLORS='*.swp=00;44;37:*,v=5;34;93:*.vim=35:no=0:fi=0:di=32:ln=36:or=1;40:mi=1;40:pi=31:so=33:bd=44;37:cd=44;37:ex=35:*.jpg=1;32:*.jpeg=1;32:*.JPG=1;32:*.gif=1;32:*.png=1;32:*.jpeg=1;32:*.ppm=1;32:*.pgm=1;32:*.pbm=1;32:*.c=1;32:*.C=1;33:*.h=1;33:*.cc=1;33:*.awk=1;33:*.pl=1;33:*.gz=31:*.tar=31:*.zip=31:*.lha=1;31:*.lzh=1;31:*.arj=1;31:*.bz2=31:*.tgz=31:*.taz=1;31:*.html=36:*.htm=1;34:*.doc=1;34:*.txt=1;34:*.o=1;36:*.a=1;36'
typeset -TUg LS_COLORS ls_colors

ls_colors=(
    # Standard Descriptors.
    'no=00'                                 # Normal
    'fi=00'                                 # Files
    'di=(01);(38;05;63)'                    # Directories
    'ln=(04);(38;05;44)'                    # Links
    'pi=(38;05;88)'                         # Named Pipes
    'so=(38;05;252)'                        # Sockets
    'bd=(38;05;237)'                        # Block Devices
    'cd=(38;05;243)'                        # Character Devices
    'or=(01);(38;05;196)'                   # ???
    'mi=(01;05);(38;05;196)'                # Missing Files
    'ex=(03);(38;05;46)'                    # Executables

    # Files, by extension.

    # Documents
    '*.pdf=(38;05;208)'

    # Images
    '*.bmp=(38;05;51)'
    '*.gif=(38;05;51)'
    '*.jpg=(38;05;51)'
    '*.png=(38;05;51)'
    '*.svg=(38;05;51)'
    '*.tif=(38;05;51)'
    '*.xbm=(38;05;51)'
    '*.xpm=(38;05;51)'

    # Audio
    '*.mp3=(38;05;141)'
    '*.ogg=(38;05;141)'
    '*.wav=(38;05;141)'
    '*.wma=(38;05;141)'

    # Video
    '*.avi=(38;05;61)'
    '*.mkv=(38;05;61)'
    '*.divx=(38;05;61)'
    '*.mp4=(38;05;61)'
    '*.xvid=(38;05;61)'

    # Archives
    '*.7z=(38;05;162)'
    '*.Z=(38;05;162)'
    '*.ace=(38;05;162)'
    '*.arj=(38;05;162)'
    '*.bz2=(38;05;162)'
    '*.bz=(38;05;162)'
    '*.cpio=(38;05;162)'
    '*.deb=(38;05;162)'
    '*.gz=(38;05;162)'
    '*.lzh=(38;05;162)'
    '*.rpm=(38;05;162)'
    '*.tar=(38;05;162)'
    '*.taz=(38;05;162)'
    '*.tgz=(38;05;162)'
    '*.tz=(38;05;162)'
    '*.z=(38;05;162)'
    '*.zip=(38;05;162)'
)

export LS_COLORS

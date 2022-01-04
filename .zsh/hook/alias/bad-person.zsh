# Alice's over-engineered z-shell configuration, released in the public domain.
# Yes, I'm a bad person.

alias 4ch='rm -f ~/.4ch-cookies; touch ~/.4ch-cookies; wget -e robots=off -E -nd -nc -np -r -H -Di.4cdn.org -Rhtml --user-agent="Mozilla/5.0 (X11; U; Linux i686; es-AR; rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" --header="Accept-Language: es-ar,es;q=0.8,en-us;q=0.5,en;q=0.3" --header="Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7" --header="Keep-Alive: 300" --header="Connection: keep-alive" --load-cookies ~/.4ch-cookies --save-cookies ~/.4ch-cookies --keep-session-cookies'

alias dch='rm -f ~/.dch-cookies; touch ~/.dch-cookies; wget -e robots=off -E -nd -nc -np -r -H -Ddesuchan.net -Rhtml --user-agent="Mozilla/5.0 (X11; U; Linux i686; es-AR; rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" --header="Accept-Language: es-ar,es;q=0.8,en-us;q=0.5,en;q=0.3" --header="Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7" --header="Keep-Alive: 300" --header="Connection: keep-alive" --load-cookies ~/.dch-cookies --save-cookies ~/.dch-cookies --keep-session-cookies'

alias ydl="yt-dlp -o '%(upload_date)s--%(id)s--%(title)s--%(resolution)s.%(ext)s' --progress --concurrent-fragments 3 --continue --ignore-errors --restrict-filenames --no-overwrites --no-playlist --xattr-set-filesize --write-info-json --paths temp:/tmp/cast --no-call-home --no-mark-watched --format '700+140/699+140/299+140/bestvideo[ext=mp4]+bestaudio[ext=m4a]' --merge-output-format mp4 --embed-subs --embed-metadata --embed-thumbnail --sub-format best --sub-langs all"

function yd() {
	yt-dlp -o '%(upload_date)s--%(id)s--%(title)s--%(resolution)s.%(ext)s' --progress --concurrent-fragments 3 --continue --ignore-errors --restrict-filenames --no-overwrites --no-playlist --xattr-set-filesize --write-info-json --paths temp:/tmp/cast --no-call-home --no-mark-watched --format '700+140/699+140/299+140/bestvideo[ext=mp4]+bestaudio[ext=m4a]' --merge-output-format mp4 --embed-subs --embed-metadata --embed-thumbnail --sub-format best --sub-langs all "https://youtube.com/watch?v=$1"
}

# alias ydl1080="youtube-dl --ignore-errors --download-archive _archive.ids --no-mark-watched --no-playlist --restrict-filenames --continue --no-overwrites --write-description --write-info-json --write-thumbnail --no-call-home --write-sub --embed-subs -o '%(playlist)s/%(upload_date)s--%(id)s--%(title)s--%(resolution)s.%(ext)s' --merge-output-format mp4 --sub-format best --add-metadata --youtube-skip-dash-manifest --format '137+140/bestvideo[ext=mp4]+bestaudio[ext=m4a]'"

# alias ydl4k="youtube-dl --ignore-errors --download-archive _archive.ids --no-mark-watched --no-playlist --restrict-filenames --continue --no-overwrites --write-description --write-info-json --write-thumbnail --no-call-home --write-sub --embed-subs -o '%(playlist)s/%(upload_date)s--%(id)s--%(title)s--%(resolution)s.%(ext)s' --merge-output-format mp4 --sub-format best --add-metadata --youtube-skip-dash-manifest --format '401+bestaudio[ext=m4a]/400+bestaudio[ext=m4a]/137+140/bestvideo[ext=mp4]+bestaudio[ext=m4a]'"
	
# alias crdl="youtube-dl --ignore-errors --download-archive _archive.ids --no-playlist --restrict-filenames --continue --no-overwrites --no-call-home --sub-format best --sub-lang enUS --embed-subs -o '%(playlist)s/%(upload_date)s--%(id)s--%(title)s--%(resolution)s.%(ext)s' --merge-output-format mp4 --add-metadata --format best --quiet --console-title"

# alias coil="curl -A 'Mozilla/4.5 (compatible; iCab 2.5.3; Macintosh; I; PPC)'"

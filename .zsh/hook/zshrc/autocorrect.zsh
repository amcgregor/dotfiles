# Enable autocompletion, but not for specific commands:

for cmd (
	brew
	ebuild
	man
	mkdir
	mv
	sudo
); do
		[[ -n $commands[$cmd] ]] && alias $cmd="nocorrect $cmd"
done

setopt correct_all

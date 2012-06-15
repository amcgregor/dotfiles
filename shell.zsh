# Alice's over-engineered z-shell configuration, released in the public domain.
# Core shell configuraiton.

typeset -A shellopts

shellopts[preexec]=1      # Run preexec to update screen title and titlebar
shellopts[screen_names]=1 # Dynamically change window names in GNU screen
shellopts[titlebar]=1     # Whether the titlebar can be dynamically changed
shellopts[utf8]=1         # Set up a few programs for UTF-8 mode

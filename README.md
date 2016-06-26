# Alice's Dotfiles

These are a small collection of miscellaneous configuration files for GNU/Linux, BSD, or otherwise UN*X-ish software. To use:

### 1. Obtain a copy of this repository.

```sh
git clone https://github.com/amcgregor/dotfiles.git
cd dotfiles
```

This should be done where you maintain your other git repositories, such as ~/Projects. Where ~/Projects is mentioned, substitute with the actual path to your holding directory like /Applications/MAMP/htdocs/dotfiles/.

### 2. Initialize and update submodules.

```sh
git submodule init
git submodule update
```

### 3. Update with your existing local files.

```sh
cp -rv ~/.config ~/.git ./
```

### 4. Remove older files.

```sh
rm -rf ~/.{byobu,config,git,vim,zsh}
```

### 5. Symlink the contents into your home folder.

```sh
ln -sf ~/Projects/.[a-z]* ~/
```

## Configuration

One major configuration directive should be customized by each user: your timezone. Update `.zsh/hook/zprofile/timezone.zsh` to set your own.

## If you are on Mac...

You'll want a copy of Homebrew, then use it to get a copy of zsh.

```sh
brew install zsh ack
sudo vim /etc/shells  # add the line: /usr/local/bin/zsh
```

Exit vim by ESC out of input mode then :wq

Then go to System Preferences, Users & Groups. Right-click your account, click the lock to enable changes, select Advanced Options, then set your shell to `/usr/local/bin/zsh`.


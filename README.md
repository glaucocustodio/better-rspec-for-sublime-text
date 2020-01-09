# RSpec Buddy

A small Sublime Text package to boost your productivity when using RSpec.

A modified fork of https://github.com/fnando/better-rspec-for-sublime-text.

## Features

### Inherited from Better RSpec

- command and shortcut for toggling between implementation/spec files ([see demo](#toggling-between-implementationspec))
- syntax highlighting

### RSpec Buddy exclusive ⭐️

- `describe` block generation for each of your classes and methods when creating a new spec file ([see demo](#toggling-between-implementationspec))
- configuration file
- some handy little tweaks

#### Toggling between implementation/spec

![alt tag](https://raw.githubusercontent.com/glaucocustodio/rspec-buddy-for-sublime-text/master/rspec_toggle_demo_v2.gif)

The default binding is `super+.`.

```json
{
  "keys": ["super+."],
  "command": "rspec_toggle"
}
```

You can change it to whatever you want by adding the following snippet to your Keybindings file.

```json
{
  "keys": ["ctrl+alt+down"],
  "command": "rspec_toggle"
}
```

#### Describe block generation
- infers the class/module name from the implementation file path to put at `RSpec.describe`
- creates a `describe` block for each method from the implementation file

#### Configuration file
Reads an optional `.rspec-buddy` file so you can customize the path to ignore when looking for spec and implementation files

Suppose you have the following structure:

```
project/
  lib/
    whatever/
      file.rb
  spec/
    file_spec.rb
```
By invoking the `rspec_toggle` command, this plugin will look for the spec file at `project/spec/whatever/file_spec.rb`(by default `lib/` will always be ignored).

But you can create a `project/.rspec-buddy` file with the content `lib/whatever/` for instance, then, the plugin will look for the spec file at `project/spec/file_spec.rb` (ignoring `lib/whatever/`).

#### Handy tweaks
- does not add `require 'spec_helper'`/`require 'rails_helper'` to spec files as you can keep your tests clean by putting them in the `.rspec` file.
- remove all snippets from the Better RSpec as I believe you should create the ones you like.

#### Syntax Detection

The best way of setting the syntax automatically is using the [ApplySyntax](https://sublime.wbond.net/packages/ApplySyntax) package. Just install it and you're done!

## Installation

### Package Control

1. Open the Command Palette (<kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>p</kbd>) and choose “*Install Package*”
2. Select “*RSpec Buddy*” and press <kbd>Enter</kbd>

### Using Git

1. Change to your Sublime Text `Packages` directory
2. Clone repository `git clone https://github.com/glaucocustodio/rspec-buddy-for-sublime-text.git 'RSpec Buddy'`

## Similar packages

- [Minitest Buddy](https://github.com/glaucocustodio/minitest-buddy-for-sublime-text)

## License

The gem is available as open source under the terms of the MIT License.

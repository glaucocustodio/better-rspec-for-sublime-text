# RSpec Buddy

RSpec syntax highlighting, implementation/spec toggling command, snippets and support for config file.

A modified fork of https://github.com/fnando/better-rspec-for-sublime-text.

What is different?

- it reads a `.rspec-buddy` file so you can customize the path to ignore when looking for spec and implementation files
- it has less snippets (just the ones I use often)
- some handy little tweaks

## .rspec-buddy file

Suppose you have the following structure:

```
project/
  lib/
    whatever/
      file.rb
```
By invoking the `rspec_toggle` command, this plugin will look for the spec file at `project/spec/whatever/file_spec.rb`.

But you can create a `project/.rspec-buddy` file with the content `lib/whatever/` for instance, then, the plugin will look for the spec file at `project/spec/file_spec.rb` (ignoring `lib/whatever/`).

This file is optional, by default `lib/` will be ignored.

## Toggling between implementation/spec

The default binding is `super+.`.

```json
{
  "keys": ["super+."],
  "command": "rspec_toggle"
}
```

You can change it to whatever you by adding the following snippet to your Keybindings file.

```json
{
  "keys": ["ctrl+alt+down"],
  "command": "rspec_toggle"
}
```

## Syntax Detection

The best way of setting the syntax automatically is using the [ApplySyntax](https://sublime.wbond.net/packages/ApplySyntax) package. Just install it and you're done!

## License

The MIT License (MIT)

Copyright (c) 2018 Glauco Custódio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

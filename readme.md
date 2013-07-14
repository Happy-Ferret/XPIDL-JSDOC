# XPIDL-JSDOC

Covert from [XPIDL](https://developer.mozilla.org/en-US/docs/XPIDL "XPIDL") to JSDoc.

It's very dirty script.

* [mozilla-central mozilla/netwerk/base/public/](http://mxr.mozilla.org/mozilla-central/source/netwerk/base/public/ "mozilla-central mozilla/netwerk/base/public/")

## Installation

1. Download [xulrunner sdk](http://ftp.mozilla.org/pub/mozilla.org/xulrunner/releases/ "Index of /pub/mozilla.org/xulrunner/releases")
2. Overwrite ``xulrunner-sdk/sdk/bin`` directory with this project

## Usage

e.g)

	 python sdk/bin/jsdoc.py --cachedir=cahce -o base.h -I idl idl/<IDL_NAME>


## Contributing

The Easiest Fastest Way to Rewrite The Script.

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

The BSD 3-Clause License 

## copyright notice

```
# Copyright 2010,2011 Mozilla Foundation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE MOZILLA FOUNDATION ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE MOZILLA FOUNDATION OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation
# are those of the authors and should not be interpreted as representing
# official policies, either expressed or implied, of the Mozilla
# Foundation.
```
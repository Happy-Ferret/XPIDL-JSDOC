# XPIDL-JSDOC

Covert [XPIDL](https://developer.mozilla.org/en-US/docs/XPIDL "XPIDL") to JSDoc.

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

MIT
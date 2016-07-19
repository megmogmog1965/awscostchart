var dest = './static';
var build = './build';
var src = './src';
var path = require('path');
var relativeSrcPath = path.relative('.', src);

module.exports = {
  tsd: {
    json: src + '/tsd.json'
  },

  tsc: {
    src: src + '/**/*.{ts,tsx}',
    dest: build
  },

  copy: {
    src: src,
    dest: dest
  },

  browserify: {
    entry: {
      entries: build + '/ts/app.js',
      debug: true
    },
    dest: dest + '/js',
    output: {
      filename: 'bundle.js'
    }
  },

  minify: {
    src: dest + '/js/bundle.js',
    filename: 'bundle.js',
    dest: dest + '/js'
  },

  watch: {
    ts: relativeSrcPath + '/ts/*.ts',
    js: relativeSrcPath + '/js/*.js'
  },

  clean: {
    dirs: [dest, build]
  }
}

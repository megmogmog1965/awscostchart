var dest = './static';
var src = './src';
var path = require('path');
var relativeSrcPath = path.relative('.', src);

module.exports = {
  tsc: {
    src: src + '/**/*.{ts,tsx}',
    dest: dest
  },

  copy: {
    src: src,
    dest: dest
  },

  browserify: {
    entry: {
      entries: dest + '/ts/app.js',
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

  clean: {
    dirs: [dest]
  }
}

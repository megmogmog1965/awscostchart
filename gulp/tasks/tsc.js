var gulp = require('gulp');
var config = require('../config');
var shell = require('gulp-shell');

// gulp.task('tsc', shell.task([
//   'tsc'
// ]));

var gulp = require('gulp'),
  typescript = require('typescript'),
  ts = require('gulp-typescript'),
  browserify = require('browserify'),
  source = require('vinyl-source-stream');

var project = ts.createProject('tsconfig.json', {
  typescript: typescript
});

gulp.task('tsc', function() {
  var result = gulp.src(config.tsc.src)
    .pipe(ts(project));
  return result.js.pipe(gulp.dest(config.tsc.dest));
});

// gulp.task('bundle', ['tsc'], function() {
//   // srcから受け取ったファイルをbrowserifyして返す関数を定義
//   // @see http://takahashifumiki.com/web/programing/3512/
//   var browserified = transform(function(filename) {
//     var b = browserify(filename);
//     b.add(filename);
//     return b.bundle();
//   });
//
//   return gulp.src('src/**/*.js')
//     .pipe(browserified) // ここで指定する
//     .pipe(source('bundle.js'))
//     .pipe(gulp.dest('dist'));
// });

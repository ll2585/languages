'use strict';

var gulp = require('gulp');
// Requires the gulp-sass plugin
var sass = require('gulp-sass');
var browserSync = require('browser-sync');
var runSequence = require('run-sequence');

gulp.task('sass', function(){
  return gulp.src('scss/**/*.scss')
    .pipe(sass()) // Converts Sass to CSS with gulp-sass
    .pipe(gulp.dest('static/stylesheets/'))
    .pipe(browserSync.reload({
      stream: true
    }))
});

gulp.task('js-watch', [], browserSync.reload);

gulp.task('watch', ['browserSync', 'sass'], function(){
  gulp.watch('scss/**/*.scss', ['sass']);
  // Other watchers
    gulp.watch('static/**/*.html', [browserSync.reload]);
    gulp.watch('static/**/*.js', ['js-watch']);
});

gulp.task('browserSync', function() {
  browserSync({
    proxy: "127.0.0.1:5000/hanja"
  })
});


gulp.task('default', function (callback) {
  runSequence(['sass','browserSync', 'watch'],
    callback
  )
});
var gulp = require('gulp');
var path = require('path');
var source = path.join('.', 'macros', '**', '*');
var destination = '\\NatLink\\NatLink\\MacroSystem';

gulp.task('copy-macros', function () {
  console.log("copying macros");
  gulp.src(source).pipe(gulp.dest(destination));
});

gulp.task('default', function () {
  gulp.run('copy-macros');
  gulp.watch(source, function (event) {
    gulp.run('copy-macros');
  });
});

const glob = require('glob');
const { SCSS_DIRS_PATH, compileSass } = require('./_sass');


// Retrives every SASS directory in project
const scssDirs = glob.sync(SCSS_DIRS_PATH);

// Compiles each retrived SCSS file to CSS
scssDirs.forEach((scssDir) => compileSass(scssDir));
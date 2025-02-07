const glob = require('glob');
const { SCSS_DIRS_PATH, watchSass } = require('./_sass');


// Retrives every SASS directory in project
const scssDirs = glob.sync(SCSS_DIRS_PATH);

// Starts watching each retrived SCSS file for changes
scssDirs.forEach((scssDir) => watchSass(scssDir));
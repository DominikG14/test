const glob = require('glob');
const { SCSS_FILES_PATH, importSass } = require('./_sass');


// Retrives every SASS file in project
const scssFiles = glob.sync(SCSS_FILES_PATH);

// Adds preambule at the top of each retrived file if it's not already there
scssFiles.forEach((scssFile) => importSass(scssFile));
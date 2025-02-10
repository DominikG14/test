const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { SCSS_FILES_PATH, SCSS_DIRS_PATH, CSS_DIRS_PATH, SASS_MODULES_PATH, SASS_IMPORT } = require('./_const');


/**
 * Compiles SCSS to CSS
 * @param {string} scssDir - Path to the directory containing SCSS
 * @returns {void} No return value
 */
function compileSass(scssDir){
  const stylesDir = path.join(scssDir, CSS_DIRS_PATH);
  const command = `sass ${scssDir}:${stylesDir} --load-path=${SASS_MODULES_PATH} --style=expanded --no-source-map`;
  exec(command);
}

/**
 * Starts watching and compiles SCSS to CSS at every change
 * @param {string} scssDir - Path to the directory containing SCSS
 * @returns {void} No return value
 */
function watchSass(scssDir){
  const stylesDir = path.join(scssDir, CSS_DIRS_PATH);
  const command = `sass --watch ${scssDir}:${stylesDir} --load-path=${SASS_MODULES_PATH} --style=expanded --no-source-map`;
  exec(command);
}

/**
 * Adds '@use "sass" as *'  preambule at the top of the file.
 * If the preambule is already there leaves the file unchanged.
 * @param {string} scssFile - Path to the SCSS file
 * @returns {void} No return value
 */
function importSass(scssFile) {
  fs.readFile(scssFile, 'utf8', (err, data) => {
    // Check if import is already at the top
    if (data.startsWith(SASS_IMPORT)) return;

    // Combine the import to be added with the current content
    const newData = `${SASS_IMPORT}\n${data}`;
    fs.writeFile(scssFile, newData, 'utf8', (err) => {});
  });
}


module.exports = { 
  SCSS_FILES_PATH,
  SCSS_DIRS_PATH,
  CSS_DIRS_PATH,
  watchSass,
  compileSass,
  importSass,
};

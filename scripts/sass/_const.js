const path = require('path');


/**
 * Path to SCSS directories
 * @type {string}
 */
const SCSS_DIRS_PATH = 'project/static/*/scss';

/**
 * Path to compiled CSS directories (Relitve to 'scss' directory)
 * @type {string}
 */
const CSS_DIRS_PATH = '../styles';

/**
 * Path to the directory where main 'sass' directory is located (Relitve to 'scripts' directory)
 * @type {string}
 */
const SASS_MODULES_PATH = 'project/sass';

/**
 * Preambule at the top of each SCSS file
 * @type {string}
 */
const SASS_IMPORT = '@use "sass" as *;';

/**
 * Path to the SCSS files
 * @type {string}
 */
const SCSS_FILES_PATH = 'project/static/*/scss/*.scss';


module.exports = { 
  SCSS_FILES_PATH,
  SCSS_DIRS_PATH,
  CSS_DIRS_PATH,
  SASS_MODULES_PATH,
  SASS_IMPORT,
};
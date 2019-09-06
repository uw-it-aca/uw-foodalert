const path = require("path");

module.exports = (function(settings) {
    settings.globals.visual_regression_settings.generate_screenshot_path =
        generateScreenshotFilePath;
    return settings;
})(require('./nightwatch.json'));
  

function generateScreenshotFilePath(nightwatchClient, basePath, fileName) {
    const moduleName = nightwatchClient.currentTest.module,
        testName = nightwatchClient.currentTest.name

    return path.join(process.cwd(), basePath, moduleName, testName, fileName)
}
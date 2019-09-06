module.exports = {
  'Host Welcome Page Test': function(browser) {
    browser
        .url('http://food:8000/h/welcome');

    browser.waitForElementVisible('body');

    browser.getTitle(function(title) {
      browser.assert.equal(
          title,
          'Share your leftover event food - Hungry Husky'
      );
    });

    browser.assert.screenshotIdenticalToBaseline('nav', 'h-welcome')

    browser.click('a.btn').pause(100);

    browser.getTitle(function(title) {
      browser.assert.equal(
          title,
          'Help us determine if your food is shareable'
      );
    });

    browser.assert.screenshotIdenticalToBaseline('nav', 'h-welcome')

    browser.back().pause(200).getTitle(function(title) {
      browser.assert.equal(
          title,
          'Share your leftover event food - Hungry Husky'
      );
    });

    browser.window()

    browser.assert.screenshotIdenticalToBaseline('nav', 'h-welcome')

    browser.end();
  },
};

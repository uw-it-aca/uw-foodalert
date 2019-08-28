module.exports = {
  'Host Welcome Page Test': function(browser) {
    browser.pause(50000);
    browser
        .url('http://localhost:8000/h/welcome');

    browser.waitForElementVisible('body');

    browser.getTitle(function(title) {
      this.assert.equal(title, 'Share your leftover event food - Hungry Husky');
    }.bind(this));

    browser.click('button').pause(100);

    browser.getTitle(function(title) {
      this.assert.equal(title, 'Help us determine if your food is shareable');
    }.bind(this));

    browser.back().pause(200).getTitle(function(title) {
      this.assert.equal(title, 'Share your leftover event food - Hungry Husky');
    }.bind(this));

    browser.end();
  },
};

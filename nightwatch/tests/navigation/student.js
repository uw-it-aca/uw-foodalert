module.exports = {
    'Step one of two: Student Welcome Page': function(browser) {
        browser
            .url('http://food:8000/s/welcome')
            .waitForElementVisible('body', 1000)
            .getTitle(function(title) {
                browser.assert.equal(
                    title,
                    'Find surplus food on campus'
                );
            })
            .assert.screenshotIdenticalToBaseline('body', 's-welcome');
    },

    'Step two of two: Navigate to Responsibilities page': function(browser) {
        browser
            .click('a.btn').pause(100)
            .getTitle(function(title) {
                browser.assert.equal(
                    title,
                    'Terms of service'
                );
            })
            .assert.screenshotIdenticalToBaseline('body', 's-responsibilities')
            .end()
    },

    'Unagreed Responsibilities Page Test': function(browser) {
        // try to navigate to next page without agreeing to terms
        browser
            .url('http://food:8000/s/responsibilities')
            .waitForElementVisible('body', 1000)
            .click('#s-agree').pause(100)
            .getTitle(function(title) {
                browser.assert.equal(
                    title,
                    'Terms of service'
                );
            })
            .assert.screenshotIdenticalToBaseline('body', 's-error-resp')
            .end();
    },

    'Agreed Responsibilities Page Test': function(browser) {
        browser
            .url('http://food:8000/s/responsibilities')
            .getTitle(function(title) {
                browser.assert.equal(
                    title,
                    'Terms of service'
                );
            })
            .assert.screenshotIdenticalToBaseline('body', 's-responsibilities');
        
        var checkBoxId = null;
        var self = browser;
        
        

        browser
            .assert.elementPresent('#cond1')
            .element('id', 'cond1', function(response) {
                checkBoxId = response.value.ELEMENT;
                self.elementIdSelected(checkBoxId, function(result) {
                    self.assert.equal(result.value, false, 'CheckBox is not checked');
                });
            })
            .click('label[for="cond1"]')
            .element('id', 'cond1', function(response) {
                checkBoxId = response.value.ELEMENT;
                self.elementIdSelected(checkBoxId, function(result) {
                    self.assert.equal(result.value, true, 'CheckBox1 is checked');
                });
            })
            .assert.elementPresent('#cond2')
            .element('id', 'cond2', function(response) {
                checkBoxId = response.value.ELEMENT;
                self.elementIdSelected(checkBoxId, function(result) {
                    self.assert.equal(result.value, false, 'CheckBox1 is not checked');
                });
            })
            .click('label[for="cond2"]')
            .element('id', 'cond2', function(response) {
                checkBoxId = response.value.ELEMENT;
                self.elementIdSelected(checkBoxId, function(result) {
                    self.assert.equal(result.value, true, 'CheckBox1 is checked');
                });
            });

        browser.assert.screenshotIdenticalToBaseline('body', 's-all-agreed-resp');

        browser
            .click('#s-agree').pause(100)
            .getTitle(function(title) {
                browser.assert.equal(
                    title,
                    'Choose how you want to be notified'
                );
            })
            .assert.screenshotIdenticalToBaseline('body', 's-notifications')
            .end();
    }
};
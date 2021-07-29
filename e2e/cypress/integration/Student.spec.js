import { verify } from "crypto"

describe('Student Tests', function() {
  it('Work Flow 1/2', function() {
    cy.visit('/s/welcome')
    cy.title().should('eq', 'Find surplus food on campus')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('a.button-text').click()
    cy.title().should('eq', 'Terms of service')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()
  })

  it('Input Validation', function() {
    cy.get('button.button-text').click()
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('label.custom-control-label').first().click()
    cy.get('input').first().should('be.checked')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.reload()

    cy.get('label.custom-control-label').first().click()
    cy.get('input').first().should('be.checked')
    cy.get('label.custom-control-label').first().click()
    cy.get('input').first().should('not.be.checked')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()
  })

  it('Work Flow 2/2', function() {
    cy.reload()
    cy.get('label.custom-control-label').each(($el, index, $list) => {
      cy.wrap($el).click()
    })
    cy.get('input').each(($el, index, $list) => {
      cy.wrap($el).should('be.checked')
    })
    cy.wait(1000)
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('button.button-text').click()
    cy.title().should('eq', 'Choose how you want to be notified')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()
  })
})

describe('Notifiction Preferences', function() {
  it('checks user preferences - email', function() {
    cy.visit('/s/notifications')
    cy.title().should('eq', 'Choose how you want to be notified')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('.custom-control.custom-switch').eq(1).click()
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('.custom-control.custom-switch').eq(1).click()
    // cy.document().toMatchImageSnapshot()ImageSnapshot()
  })

  it('checks user preferences - phone', function() {
    cy.visit('/s/notifications')
    cy.title().should('eq', 'Choose how you want to be notified')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('.custom-control.custom-switch').eq(0).click()
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('a.btn-link').eq(1).click()
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('#text-add-input').type('2011111111')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('button.btn-primary').click()
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('#text-add-input').type('{backspace}{backspace}{backspace}{backspace}{backspace}{backspace}{backspace}{backspace}{backspace}{backspace}')

    cy.get('#text-add-input').type('8042221111')
    // cy.document().toMatchImageSnapshot()ImageSnapshot()

    cy.get('button.btn-primary').click()
    cy.wait(1000)
    // cy.document().toMatchImageSnapshot()ImageSnapshot()
  })
})
describe('My First Test', function() {
  it('FoodTase', function() {
    cy.visit('/s/welcome')
    cy.title().should('eq', 'Find surplus food on campus')
    cy.document().toMatchImageSnapshot()
  })
})
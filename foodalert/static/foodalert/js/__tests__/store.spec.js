import {mutations} from '../store.js';

describe('vuex store allows users to', function() {
    var state;

    beforeEach(function() {
        state = {
            claimsPermit: false,
            permitNumber: null,
            onSafeList: false,
            safeFoodList: [],
            acceptedSafeListTerms: false,
        };
    });

    describe.each([true, false])('claim permit', function(claimedPermit) {
        beforeEach(function() {
            state.claimsPermit = claimedPermit;
        });

        test('user can claim permit', function() {
            mutations.claimPermit(state);
            expect(state.claimsPermit).toBeTruthy();
        });

        test('user can relinquish permit', function() {
            mutations.relinquishPermit(state);
            expect(state.claimsPermit).toBeFalsy();
        });
    });

    var permitNumbers = [
        null,
        undefined,
        0,
        123456,
        Number.MAX_SAFE_INTEGER,
        Number.MIN_SAFE_INTEGER
    ];
    describe.each(permitNumbers)('set permit number', function(initialNumber) {
        beforeEach(function() {
            state.permitNumber = initialNumber;
        });

        test.each(permitNumbers)('from '+ initialNumber+ ' to %p', function(finalNumber) {
            mutations.setPermitNumber(state, finalNumber);
            expect(state.permitNumber).toEqual(finalNumber);
        });
    });

    describe.each([true, false])('claim food on safe list', function(claimedSafeList) {
        beforeEach(function() {
            state.onSafeList = claimedSafeList;
        });

        test('user can claim food is on the safe list', function() {
            mutations.claimSafeFood(state);
            expect(state.onSafeList).toBeTruthy();
        });

        test('user can relinquish safe list claim', function() {
            mutations.relinquishSafeFood(state);
            expect(state.claimsPermit).toBeFalsy();
        });
    });

    var possibleFoods = [
        null,
        undefined,
        [[]],
        [["food"]],
        [["food #1", "Food #2"]],
    ];
    describe.each(possibleFoods)('set the food list', function(initialFood) {
        beforeEach(function() {
            state.safeFoodList = initialFood;
        });

        test.each(possibleFoods)('from ' + initialFood + ' to %s', function(finalFoods) {
            mutations.setSafeFoods(state, finalFoods);
            expect(state.safeFoodList).toEqual(finalFoods);
        });
    });

    describe.each([true, false])('accept the safe food list terms', function(claimedSafeList) {
        beforeEach(function() {
            state.acceptedSafeListTerms = claimedSafeList;
        });

        test('user can claim food is on the safe list', function() {
            mutations.acceptSafeListTerms(state);
            expect(state.acceptedSafeListTerms).toBeTruthy();
        });

        test('user can reject safe list claim', function() {
            mutations.rejectSafeListTerms(state);
            expect(state.acceptedSafeListTerms).toBeFalsy();
        });
    });
});

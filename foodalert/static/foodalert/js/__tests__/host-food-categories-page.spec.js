"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount, shallowMount} from '@vue/test-utils';
import FoodCategoriesPage from '../pages/host/food-categories-page.vue';

const $router = {
    push: jest.fn(),
}

describe('Food Categories Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(FoodCategoriesPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
	
	test('testing options - no option selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('testing options - first option selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
            const checkboxes = wrapper.findAll('input[type="checkbox"]') 
	    checkboxes.at(0).setChecked()
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('testing options - second option selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
            const checkboxes = wrapper.findAll('input[type="checkbox"]') 
	    checkboxes.at(1).setChecked()
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('testing options - third option selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
            const checkboxes = wrapper.findAll('input[type="checkbox"]') 
	    checkboxes.at(2).setChecked()
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('testing options - third option selected when other options were selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
            const checkboxes = wrapper.findAll('input[type="checkbox"]') 
	    checkboxes.at(0).setChecked()
	    checkboxes.at(1).setChecked()
	    checkboxes.at(2).setChecked()
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('testing options - none option selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
            const checkboxes = wrapper.findAll('input[type="checkbox"]') 
	    checkboxes.at(3).setChecked()
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('testing options - none option selected when other options were selected', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
            const checkboxes = wrapper.findAll('input[type="checkbox"]') 
	    checkboxes.at(0).setChecked()
	    checkboxes.at(1).setChecked()
	    checkboxes.at(2).setChecked()
	    checkboxes.at(3).setChecked()
	    const button = wrapper.findAll('button').at(0)
	    button.trigger('click')
	});

	test('back button', function () {
	    var wrapper = mount(FoodCategoriesPage, {
	        mocks: { $router }
	    });
	    const button = wrapper.findAll('button').at(1)
	    button.trigger('click')
	});
})

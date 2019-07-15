"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import FormPage from '../pages/host/form-page.vue';

jest.mock('axios', () => ({
	get: jest.fn((data) => Promise.resolve({data: []})),
	post: jest.fn(() => Promise.resolve())
}))

import axios from 'axios'

const $routes = {
    push: jest.fn()
}

describe('Food Categories Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(FormPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });

	test('form submit', function () {
	    var wrapper = mount(FormPage, {
	        $routes
	    });
	    var inputs = wrapper.findAll('input')
	    inputs.at(0).setValue("some random value")
	    inputs.at(1).setValue("some random value")
	    inputs.at(2).setValue("12:00 AM")
	    inputs.at(3).setValue("some random value")

	    var textarea = wrapper.find('textarea')
	    textarea.setValue("some random value")

	    var buttons = wrapper.findAll('button')
	    buttons.at(0).trigger('click')
	    buttons.at(4).trigger('click')
	});

	test('reset test', function () {
	    var wrapper = mount(FormPage, {
	        $routes
	    });

	    var buttons = wrapper.findAll('button')
	    buttons.at(1).trigger('click')
	});
})

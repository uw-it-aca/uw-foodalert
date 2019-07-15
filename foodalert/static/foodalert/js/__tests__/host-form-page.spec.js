"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import FormPage from '../pages/host/form-page.vue';

import axios from 'axios'

jest.mock('axios', () => ({
	get: jest.fn(),
	post: jest.fn()
}))

const $routes = {
    push: jest.fn()
}

describe('Food Categories Page', function () {
	test('renders correctly', function () {
		axios.get.mockImplementation(() => Promise.resolve({data: []}));
		axios.post.mockImplementation(() => Promise.resolve({data: [{name: "allergne_1"}, {name: "allergen_2"}]}));
		var wrapper = mount(FormPage, {
		});
		expect(wrapper.element).toMatchSnapshot();
	});

	test('redirect to update', function () {
		axios.get.mockImplementation(() => Promise.resolve({data: [{ended: true}]}));
		axios.post.mockImplementation(() => Promise.resolve({data: []}));
		var wrapper = mount(FormPage, {
		});
		expect(wrapper.element).toMatchSnapshot();
	});

	test('form submit', function () {
		jest.clearAllMocks()
		axios.get.mockImplementation(() => Promise.resolve({data: []}));
		axios.post.mockImplementation(() => Promise.resolve({data: []}));
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

		var form = wrapper.find("form")
		form.trigger("submit")

	    var buttons = wrapper.findAll('button')
	    // buttons.at(0).trigger('click')
		buttons.at(4).trigger('click.native')
	});

	test('reset test', function () {
		axios.get.mockImplementation(() => Promise.resolve({data: []}));
		axios.post.mockImplementation(() => Promise.resolve({data: []}));
	    var wrapper = mount(FormPage, {
	        $routes
	    });

	    var buttons = wrapper.findAll('button')
	    buttons.at(1).trigger('click')
	});
})

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
		//var temp_date = new Date('2019-05-14T11:01:58.135Z')
		//jest.spyOn(global, 'Date').mockImplementation(() => temp_date)
		wrapper.setData({form:{
			location: "",
			event: "",
			end_time: "11:11 PM",
			food_served: "",
			amount_of_food_left: "",
			bring_container: false,
			safe_foods: [],
			allergens: [],
			host_user_agent: "",
			ended: false
		}})
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
		// buttons.at(4).trigger('click.native')
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

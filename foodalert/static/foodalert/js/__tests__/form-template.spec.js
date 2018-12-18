"use strict";
import Vue from 'vue';
import Vuex from 'vuex';

import BootstrapVue from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)
Vue.use(BootstrapVue);

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon);

import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faUtensils,
    faChevronLeft,
    faCalendar,
    faClock,
    faMapMarkerAlt,
    faClipboardCheck,
    faBell,
} from '@fortawesome/free-solid-svg-icons'

library.add(faUtensils)
library.add(faChevronLeft)
library.add(faCalendar)
library.add(faClock)
library.add(faBell)
library.add(faMapMarkerAlt)
library.add(faClipboardCheck)

import {mount, createLocalVue} from '@vue/test-utils';
import FormController from '../components/form-controller.vue';

var localVue = createLocalVue();

localVue.use(Vuex);

describe('Form Controller', function () {
    var store;

    beforeEach(function () {
        store = new Vuex.Store({
            state: {},
        })
    });

    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(FormController, {
                localVue,
                store,
                propsData: {
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });
    });
})

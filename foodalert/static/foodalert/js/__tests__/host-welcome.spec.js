"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import WelcomePage from '../pages/host/welcome.vue';

describe('Welcome Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(WelcomePage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})
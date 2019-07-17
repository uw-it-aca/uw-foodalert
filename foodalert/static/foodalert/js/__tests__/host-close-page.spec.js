"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import ClosePage from '../pages/host/close-page.vue';

describe('Host Close Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(ClosePage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})
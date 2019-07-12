"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import FormPage from '../pages/host/form-page.vue';

describe('Food Categories Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(FormPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})
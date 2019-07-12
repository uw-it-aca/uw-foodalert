"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import EndedPage from '../pages/host/ended-page.vue';

describe('Host Ended Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(EndedPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})
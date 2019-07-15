"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import NeedPermitPage from '../pages/host/need-permit-page.vue';

describe('Need Permit Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(NeedPermitPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})

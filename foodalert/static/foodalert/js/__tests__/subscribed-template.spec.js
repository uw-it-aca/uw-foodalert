"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import SubscribedController from '../components/subscribed-controller.vue';

describe('Subscribed Controller', function () {
        test('renders correctly', function () {
            var wrapper = mount(SubscribedController, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})

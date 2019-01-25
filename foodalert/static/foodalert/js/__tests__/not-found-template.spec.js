"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import NotFoundTemplate from '../components/not-found-template.vue';

describe('NotFoundTemplate (404 Page)', function () {
        test('renders correctly', function () {
            var wrapper = mount(NotFoundTemplate, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})


"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import PopupContainer from '../components/popup-container.vue';

describe('Labelled Input', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(PopupContainer, {
                propsData: {
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });
    });
})

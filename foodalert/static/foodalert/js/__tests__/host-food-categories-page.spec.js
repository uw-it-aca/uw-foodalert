"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import FoodCategoriesPage from '../pages/host/food-categories-page.vue';

describe('Food Categories Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(FoodCategoriesPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})
"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import UpdateController from '../components/update-controller.vue';
const $route = {
    query: {
        parent_notification: 1
    }
}
const $v = {
    form: {
        text: {
            required: true,
            maxLength: true
        },
        $error: false
    }
}

describe('Update Controller', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(UpdateController, {
                mocks: {
                    $route,
                    $v
                },
            });
            expect(wrapper.element).toMatchSnapshot();
        });
    });
})

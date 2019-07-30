"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import NotificationPage from '../pages/student/notification-page.vue';

describe('Notification Page', function () {
        test('renders correctly', function () {
            var wrapper = mount(NotificationPage, {
            });
            expect(wrapper.element).toMatchSnapshot();
        });
})
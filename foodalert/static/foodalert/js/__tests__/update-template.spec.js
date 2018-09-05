"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faUtensils,
    faChevronLeft,
    faCalendar,
    faClock,
    faMapMarkerAlt,
    faClipboardCheck,
    faBell,
} from '@fortawesome/free-solid-svg-icons'

library.add(faUtensils)
library.add(faChevronLeft)
library.add(faCalendar)
library.add(faClock)
library.add(faBell)
library.add(faMapMarkerAlt)
library.add(faClipboardCheck)

import {mount} from '@vue/test-utils';
import UpdateTemplate from '../components/update-template.vue';

describe('Update Tempalte', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(UpdateTemplate, {
                propsData: {
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });
    });
})

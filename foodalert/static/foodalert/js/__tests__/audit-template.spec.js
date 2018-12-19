"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)
Vue.use(BootstrapVue);

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon);

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
import AuditController from '../components/audit-controller.vue';

describe('Audit Controller', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(AuditController, {
                propsData: {
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });
    });
})

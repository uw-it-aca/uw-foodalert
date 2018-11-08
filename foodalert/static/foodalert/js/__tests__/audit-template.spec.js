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
import AuditTemplate from '../components/audit-template.vue';

describe('Audit Template', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(AuditTemplate, {
                propsData: {
                    items: [{ dateSent: '10/22/18', timeSent: '4:44PM', endTime: '5:32PM', updateTime: '5:10PM', host: 'netid@uw.edu', permitNumber: '12345678', foodAndEvent: 'A Food and Event', quantity: 'About 8 meals', location: 'HUB 101', contains: 'Dairy, Meat' }]
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });
    });
})

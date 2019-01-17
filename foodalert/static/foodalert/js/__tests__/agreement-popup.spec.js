"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
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
import AgreePop from '../components/agreement-popup.vue';

describe('Agreement Popup', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(AgreePop, {
                propsData: {
                    inputType: "number",
                    mainText: "Main TExt",
                    introText: "Intro Text",
                    infoText: "Info Text",
                    linkText: "Link Text",
                    linkLocation: "www.linklocation.com",
                    primaryText: "Primary Text",
                    secondaryText: "Secondary Text",
                    canBack: true,
                    primaryAction: jest.fn(),
                    secondaryAction: jest.fn(),
                    backAction: jest.fn(),
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });

        test('checkbox', function () {
            var wrapper = mount(AgreePop, {
                propsData: {
                    inputType: "checkbox",
                    checkboxOptions: ["Option 1", "Option 2"],
                    mainText: "Main TExt",
                    introText: "Intro Text",
                    infoText: "Info Text",
                    linkText: "Link Text",
                    linkLocation: "www.linklocation.com",
                    primaryText: "Primary Text",
                    secondaryText: "Secondary Text",
                    canBack: true,
                    primaryAction: jest.fn(),
                    secondaryAction: jest.fn(),
                    backAction: jest.fn(),
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        })
    });
})

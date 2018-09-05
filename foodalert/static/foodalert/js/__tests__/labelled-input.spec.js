"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import LabelledInput from '../components/labelled-input.vue';

describe('Labelled Input', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(LabelledInput, {
                propsData: {
                    labelText: "Label Text",
                    subLabel: "Sublabel",
                    isOptional: true,
                    exampleText: "Example Text",
                    warningText: "Warning Text",
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        });

        test('checkbox', function () {
            var wrapper = mount(LabelledInput, {
                propsData: {
                    type: "checkbox",
                    labelText: "Label Text",
                    subLabel: "Sublabel",
                    isOptional: true,
                    exampleText: "Example Text",
                    warningText: "Warning Text",
                }
            });
            expect(wrapper.element).toMatchSnapshot();
        })
    });
})

"use strict";
import Vue from "vue";
import Vuex from "vuex";

import BootstrapVue from "bootstrap-vue";
import Vuelidate from "vuelidate";
Vue.use(Vuelidate);
Vue.use(BootstrapVue);

import { mount, createLocalVue } from "@vue/test-utils";
import FormController from "../components/form-controller.vue";

var localVue = createLocalVue();

localVue.use(Vuex);

describe("Form Controller", function() {
  var store;

  beforeEach(function() {
    store = new Vuex.Store({
      state: {}
    });
  });

  describe("renders correctly", function() {
    test("textarea", function() {
      var wrapper = mount(FormController, {
        localVue,
        store,
        propsData: {}
      });
      expect(wrapper.element).toMatchSnapshot();
    });
  });
});

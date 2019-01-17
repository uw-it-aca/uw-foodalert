"use strict";
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)
Vue.use(BootstrapVue);

import {mount} from '@vue/test-utils';
import AuditController from '../components/audit-controller.vue';

jest.mock('axios', function() {
    var test = {
      "data": [
        {
          "location": {
            "main": "HUB 130",
            "detail": "HUB 130"
          },
          "event": "Placeholder event",
          "time": {
            "created": "Tue Dec 18 2018 10:20:00 AM",
            "ended": "Tue Dec 18 2018 11:11:00 AM"
          },
          "food": {
            "served": "a",
            "amount": "a",
            "allergens": []
          },
          "bringContainers": false,
          "foodServiceInfo": {
            "safeToShareFood": []
          },
          "host": {
            "hostID": 1,
            "netID": "",
            "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
          }
        },
        {
          "location": {
            "main": "HUB 130",
            "detail": "HUB 130"
          },
          "event": "Placeholder event",
          "time": {
            "created": "Tue Dec 18 2018 11:08:04 AM",
            "ended": "Tue Dec 18 2018 1:00:00 PM"
          },
          "food": {
            "served": "Leftover food from HUB meeting",
            "amount": "About 8 full meals",
            "allergens": []
          },
          "bringContainers": false,
          "foodServiceInfo": {
            "safeToShareFood": []
          },
          "host": {
            "hostID": 1,
            "netID": "",
            "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
          }
        }
      ],
      "status": 200,
      "statusText": "OK",
      "headers": {
        "allow": "GET, POST, HEAD, OPTIONS",
        "content-length": "883",
        "content-type": "application/json",
        "date": "Wed, 19 Dec 2018 22:24:22 GMT",
        "server": "WSGIServer/0.2 CPython/3.6.6",
        "vary": "Accept, Cookie",
        "x-frame-options": "SAMEORIGIN"
      },
      "config": {
        "transformRequest": {},
        "transformResponse": {},
        "timeout": 0,
        "xsrfCookieName": "XSRF-TOKEN",
        "xsrfHeaderName": "X-XSRF-TOKEN",
        "maxContentLength": -1,
        "headers": {
          "Accept": "application/json, text/plain, */*"
        },
        "method": "get",
        "url": "http://0.0.0.0:8000/notification/"
      },
      "request": {}
    };
    return {
        get: function() {
            return new Promise(function(success, failure) {
                success(test);
            });
        },
    }
});

describe('Audit Controller', function () {
    describe('renders correctly', function () {
        test('textarea', function () {
            var wrapper = mount(AuditController, {
                propsData: {
                }
            });
            wrapper.vm.$on('requestComplete', function() {expect(wrapper.element).toMatchSnapshot()});
        });
    });
})

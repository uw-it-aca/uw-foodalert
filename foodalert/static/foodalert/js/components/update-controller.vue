<template>
    <update-template
        v-bind:text.sync="form.text"
        @submitRequest="this.sendUpdate"
        :v="$v"
        >
    </update-template>
</template>

<script type="text/javascript">
    import UpdateTemplate from './update-template.vue';
    import Cookies from 'js-cookie';
    import { validationMixin } from "vuelidate"
    import { required, maxLength } from "vuelidate/lib/validators"
    const axios = require('axios');

    export default {
        components: {
            'update-template': UpdateTemplate,
        },
        mounted() {
            this.state.uid = this._uid;
            this.state.notificationID = parseInt(this.$route.query.notificationID);
        },
        data() {
            return {
                state: {
                    uid: 0,
                    notificationID: 0,
                },
                form: {
                    text: ""
                },
            }
        },
        methods: {
            setText(payload) {
                this.form.text = payload;
            },
            getNotification() {
            }
            sendUpdate() {
                var data = {
                    "text": this.form.text,
                    "parent_notification": this.state.notificationID
                };
                var csrftoken = Cookies.get('csrftoken');
                var headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                }
                axios.post('/updates/', data, {"headers": headers})
                    .then(function(response) {
                        console.log(response);
                    }.bind(this))
                    .catch(function (error) {
                        console.log("There was an error processing the request");
                        console.log(error);
                    })
            }
        },
        validations: {
            form: {
                text: {
                    required,
                    maxLength: maxLength(100)
                }
            }
        },
    }   
</script>


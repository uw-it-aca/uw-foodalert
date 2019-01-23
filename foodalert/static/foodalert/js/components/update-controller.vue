<template>
    <update-template
        v-bind:text.sync="form.text"
        @submitRequest="this.sendUpdate"
        @submitEnd="this.endNotification"
        :event="this.state.event"
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
            this.getNotification();
            this.state.uid = this._uid;
        },
        data() {
            return {
                state: {
                    uid: 0,
                    notificationID: 0,
                    event: ""
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
                var headers = {
                    'Content-Type': 'application/json',
                }
                axios.get('http://0.0.0.0:8000/notification/', {"headers": headers})
                    .then(response => {
                        var data = response.data.filter(function(notif) {
                            return notif.ended == false;
                        });
                        if (data.length === 0) {
                            this.state.notificationID = 0;
                            this.state.event = "";
                        } else {
                            this.state.notificationID = data[0].id;
                            this.state.event = data[0].event;
                        }
                    })
                    .catch(error => {
                        console.log("There was an error processing the request");
                        console.log(error);
                    })
            },
            endNotification() {
                var url = '/notification/' + this.state.notificationID + '/';
                var data = {
                    "ended": true,
                };
                var csrftoken = Cookies.get('csrftoken');
                var headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                };
                this.form.text = "No Food left! The event: " + this.state.event + " has ended and is no longer serving food"
                this.sendUpdate();
                axios.patch(url, data, {"headers": headers})
                    .then(response => {
                        console.log(response);
                        this.$router.push({ name: 'ended' });
                    })
                    .catch(error => {
                        console.log(error);
                    })
            },
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


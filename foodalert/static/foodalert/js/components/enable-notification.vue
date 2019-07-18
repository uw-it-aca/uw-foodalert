<template>
    <div class="notification">
        <b-collapse :id="collapse_id" :v-model="collapse_notif">
            <b-container @click="checked=!checked">
                <b-row> 
                    <b-col sm="9" cols="9">
                        <strong>Enable notifications</strong>
                        <slot  name="message"></slot>
                        <div id="notif-status">
                            <div v-if=checked class="enabled" > Notifications are enabled</div>
                            <div v-else class="paused"> Notifications are paused </div>
                        </div>
                    </b-col>
                    
                    <b-col sm="3" cols="3" align-self="center">  
                        <b-form-checkbox 
                            v-model="checked"
                            name="enable-switch" 
                            @click.native.prevent
                            class="float-right"
                            switch>
                        </b-form-checkbox> 
                    </b-col>
                </b-row>
            </b-container>  
        </b-collapse>
    </div>
</template>

<script>
    export default {
        props: {
            collapse_id: {
                type: String,
                required: true
            },
            collapse_notif: {
                type: Boolean,
                default: true
            }
        },
        data() {
            return {
                checked: false,
            }
        },
    }
</script>

<style>
    .notification #notif-status .enabled {
        color: green;
    }

    .notification #notif-status .paused {
        color: red;
    }
    
    .notification .container {
        padding: .75rem 1.25rem;
        padding-left: 0px;
        border-top: 1px solid #9B9B9B;
    }
</style>

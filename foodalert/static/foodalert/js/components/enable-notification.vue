<template>
    <div>
        <b-collapse id="notification">
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

<script type="text/javascript">
    export default{
        data() {
            return {
                checked: false
            }
        },

        props: {
            canNotify: {
                type: Boolean,
                default: false,
            },
        }, 
        
    }
</script>

<style>
    :root {
        --switch-width: 50px;
        --switch-height: 32px;
        --switch-circle: 26px;
    }
    #notif-status .enabled {
        color: green;
    }

    #notif-status .paused {
        color: red;
    }

    .custom-switch .custom-control-label::before {
        width: var(--switch-width) !important;
        height: var(--switch-height) !important;
        border-radius: 1rem !important;
        top: 0px;
    }

    .custom-switch .custom-control-label:after {
        width: var(--switch-circle) !important;
        height: var(--switch-circle) !important;
        border-radius: 50% !important;
        top: .2rem !important;
    }

    .custom-switch .custom-control-input:checked~.custom-control-label::after {
        transform: translateX(1.2rem) !important;
    }

    .custom-control.custom-switch {
        height: var(--switch-height);
    }

    .collapse.show {
        border-top: 1px solid #9B9B9B;
    }

    #notification .container {
        padding: .75rem 1.25rem;
        padding-left: 0px;
    }

</style>

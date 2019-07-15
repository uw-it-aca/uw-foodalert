<template>
    <div>
        <b-container @click="checked=!checked">
            <b-row align-v="center"> 
                <b-col sm="10" cols="10">
                    <strong>Enable notifications</strong>
                    <slot  name="message"></slot>
                    <div id="notif-status">
                        <div v-if=checked class="enabled" > Notifications are enabled</div>
                        <div v-else class="paused"> Notifications are paused </div>
                    </div>
                </b-col>
                <b-col sm="2" cols="2"> 
                    <b-form-checkbox 
                        v-model="checked"
                        name="enable-switch" 
                        @click.native.prevent
                        switch>
                    </b-form-checkbox>
                </b-col>
            </b-row>
        </b-container>  
    </div>
</template>

<script type="text/javascript">
    import CollapseTextbox from "./collapse-text-box.vue";
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
        
        components: {
            "collapse-textbox": CollapseTextbox,
        }
        
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
    }

    .custom-switch .custom-control-label:after {
        width: var(--switch-circle) !important;
        height: var(--switch-circle) !important;
        border-radius: 50% !important;
        top: calc(.25rem + 3px) !important;
    }

    .custom-switch .custom-control-input:checked~.custom-control-label::after {
        transform: translateX(1.2rem) !important;
    }


</style>

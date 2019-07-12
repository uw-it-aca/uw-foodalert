<template>
    <div>
        <b-container>
            <b-row>
                <b-col>
                    <div style="padding: .375rem .75rem;">
                        <label><strong>Enable notifications</strong></label>
                    </div>
                </b-col>
                <b-col> 
                    <div>
                        <b-form-checkbox 
                            v-model="checked"
                            name="enable-switch"   
                            class="float-right" 
                            switch>
                        </b-form-checkbox>
                    </div>
                </b-col>
            </b-row>
            <b-row>
                <b-col >
                    <div style="padding: .375rem .75rem;">
                        <slot  name="message"></slot>
                    </div>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <div id="notif-status" >
                        <div style="padding: .375rem .75rem;">
                            <div v-if=checked class="enabled" > Notifications are enabled</div>
                            <div v-else class="paused"> Notifications are paused </div>
                        </div>
                    </div>
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
    #notif-status .enabled {
        color: green;
    }

    #notif-status .paused {
        color: red;
    }
</style>

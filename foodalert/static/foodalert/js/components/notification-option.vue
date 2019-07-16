<template>
    <b-card no-body class="notif-option-card">
      <!--b-card-header header-tag="header" class="p-1" role="tab"!-->
        <b-container slot="header" class="p-0">
            <b-row>
                <b-col cols="6">
                    <slot name="opt_heading">Placeholder Text</slot>
                </b-col>
                <b-col cols="6">
                    <b-button block href="#" v-b-toggle="accord_id" variant="link" class="opt_link_btn p-0">
                        <slot name="opt_link_0" v-if="rendering == 0">State {{rendering}}: add</slot>
                        <slot name="opt_link_1" v-else-if="rendering == 1">State {{rendering}}: cancel</slot>
                        <slot name="opt_link_2" v-else-if="rendering == 2">State {{rendering}}: edit</slot>
                        <slot name="opt_link_3" v-else-if="rendering == 3">State {{rendering}}: cancel</slot>
                        <slot name="opt_link_invalid" v-else>Placeholder Text 4</slot>
                    </b-button>
                </b-col>
            </b-row>
        </b-container>
      <!--/b-card-header!-->
      <b-collapse :id="accord_id" accordion="my-accordion" role="tabpanel" v-model="isOpen">
        <b-card-body>
            <b-container class="p-0">
                <b-row>
                    <b-col cols="12">
                        <b-card-text>
                            <b-form @submit.prevent="nextState()" v-if="state == 0">
                                <!-- this is the state for initially adding a notif !-->
                                <small class="form-text text-muted">{{label}}</small>
                                <b-form-group :description="description">
                                    <b-form-input required number :formatter="formatter" width="300px"></b-form-input>
                                </b-form-group>
                                <b-button type="submit" variant="primary" class="float-right">Verify</b-button>
                            </b-form>
                            <b-form v-else-if="state == 1">
                                <!--this is the state for updating notif !-->
                                <small class="form-text text-muted">{{label}}</small>
                                <b-form-group :description="description">
                                    <b-form-input required number :formatter="formatter" width="300px"></b-form-input>
                                </b-form-group>
                                <b-button>Delete(no funct)</b-button>
                                <b-button type="submit" variant="primary" class="float-right">Update</b-button>
                            </b-form>
                        </b-card-text>
                    </b-col>
                </b-row>
            </b-container>
        </b-card-body>
      </b-collapse>
    </b-card>
</template>

<script>
export default {
    props: {
        accord_id: String,
        label: {
            type: String,
            default: "Placeholder label",
        },
        description: {
            type: String,
            default: "Placeholder description",
        },
        type: {
            type: String,
            default: "phonenumber"
        },
        collapse_notif: Boolean,  
    },
    data() {
        return {
            state: 0,
            isOpen: false,
            states: [[0, 1], [2, 3]],
            rendering: 0,
            collapse_1: false,
            collapse_3: false,
        } 
    },
    methods: {
        formatter(value, event){
            if (this.type == "phonenumber") {
                return this.numberFormatter(value, event);
            }
        },
        numberFormatter(value, event){
            if (value.length > 14)
                return value.substr(0, 14)
            var cleaned = ('' + value).replace(/\D/g, '')
            var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
            if (match) {
                return '(' + match[1] + ') ' + match[2] + '-' + match[3];
            }
            return cleaned
        },
        nextState(){
            if(this.state < 1){ //cannot surpas max state
                this.state++;
            }
            this.isOpen = !this.isOpen;
            //emits when verify has been clicked on a notification
            this.$emit('check-collapse', this.accord_id); 
        },
        previousState() {
            if(this.state > 0){
                this.state--;
            }
        }, 
    },
    watch: {
        isOpen(newOpen, prevOpen) {
            if (newOpen) {
                this.rendering = this.states[this.state][1]
            } else {
                this.rendering = this.states[this.state][0]
            }
            this.collapse_1 = (this.rendering == 1);
            this.collapse_3 = (this.rendering == 3);
        },
    },
    computed: {
    }
}
</script>

<style>
    .notif-option-card .card-header{
        background-color: inherit !important;
        border-bottom: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .notif-option-card .text-muted{
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .notif-option-card .card-body{
        padding: 0 !important;
        padding-bottom: 10px !important;
    }
    .notif-option-card .form-group{
        margin-bottom: -10px !important;
    }
    .notif-option-card .opt_link_btn {
        text-align: right !important;
    }
    .notif-option-card {
        border-radius: 0 !important;
        border: unset !important;
        border-top: 1px solid #9B9B9B !important;
        border-bottom: 1px solid #9B9B9B !important;
    }
    .notif-option-card~.notif-option-card{
        border-top: unset !important;
    }
    .notif-option-card input.form-control~small {
        margin-top: 1px !important;
    }
    .notif-option-card .slide-fade-enter-active {
        transition: all 1s ease;
    }
    .notif-option-card .slide-fade-leave-active {
        transition: all 1s cubic-bezier(1.0, 0.5, 0.8, 1.0);
    }
</style>

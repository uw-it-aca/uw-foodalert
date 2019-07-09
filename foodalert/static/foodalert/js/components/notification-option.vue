<template>
    <b-card no-body>
      <!--b-card-header header-tag="header" class="p-1" role="tab"!-->
        <b-container slot="header">
            <b-row>
                <b-col cols="6">
                    <div style="padding: .375rem .75rem;">
                        <slot name="opt_heading">Placeholder Text</slot>
                    </div>
                </b-col>
                <b-col cols="6">
                    <b-button block href="#" v-b-toggle="accord_id" variant="link" class="opt_link_btn">
                        <slot name="opt_link_open" v-if="a">Placeholder Text</slot>
                        <slot name="opt_link_close" v-else>Placeholder Text2</slot>
                    </b-button>
                </b-col>
            </b-row>
        </b-container>
      <!--/b-card-header!-->
      <b-collapse :id="accord_id" visible accordion="my-accordion" role="tabpanel">
        <b-card-body>
            <b-container>
                <b-row>
                    <b-col cols="12" style="margin-top: -20px; margin-bottom: 10px">
                        <b-card-text>
                            <div style="padding: .375rem .75rem;">
                                <b-form>
                                    <small class="form-text text-muted">{{label}}</small>
                                    <b-form-group :description="description">
                                        <b-form-input required number :formatter="formatter" width="300px"></b-form-input>
                                    </b-form-group>
                                    <b-button type="submit" variant="primary" class="float-right">Verify</b-button>
                                </b-form>
                            </div>
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
            default: "Placeholder Text",
        },
        description: {
            type: String,
            default: "Placeholder Text",
        },
        type: {
            type: String,
            default: "phonenumber"
        }
    },
    data() {
        return {
            
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
        }                
    },
}
</script>

<style scoped>
    .card-header{
        background-color: inherit !important;
        border-bottom: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .text-muted{
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .card-body{
        padding: 0 !important;
        padding-bottom: 10px !important;
    }
    .form-group{
        margin-bottom: -10px !important;
    }
    .opt_link_btn {
        text-align: right !important;
    }
</style>

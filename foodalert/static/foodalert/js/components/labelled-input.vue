<template>
    <b-container fluid class="px-0 py-1">
        <b-form-group class="labelled-textarea mb-0" :label-for="'textarea-' + id">
            <template slot="label">
                {{ labelText }} <br />
            </template>
            <b-form-textarea
                v-if="inputType=='textarea'"
                :rows="rows"
                :class="{hasError: v.$error}"
                :placeholder="exampleText"
                :id="'textarea-' + id"
                size="md"
                v-model="v.$model"
                @input="updateStore($event)">
            </b-form-textarea>
            <b-form-input
                v-else-if="inputType=='time'"
                :class="{hasError: v.$error}"
                :placeholder="exampleText"
                :id="'time-input-' + id"
                size="md"
                v-model="v.$model"
                @input="updateStore($event)">
            </b-form-input>
            <b-form-checkbox-group
                v-else-if="inputType=='checkbox'"
                v-model="checked"
                :id="'checkbox-' + id"
                @input="updateStore($event)">
                <b-row
                    v-for="box in boxes"
                    class="mx-0">
                    <b-form-checkbox :value="box"> {{ box }} </b-form-checkbox><br>
                </b-row>
            </b-form-checkbox-group>
            <b-container
                v-else-if="inputType=='buttons'"
                v-model="checked"
                :id="'button-' + id">
                <b-button @click="updateStore(true)" variant="outline-success">Yes</b-button>
                <b-button @click="updateStore(false)" variant="outline-success">No</b-button>
            </b-container>
        </b-form-group>
        <b-alert v-if="warningText" show variant="primary" placement="bottom" class="mt-1"> {{warningText}} </b-alert>
    </b-container>
</template>

<script>
    export default {
        props: {
            v: {
                default: function() {
                   return {
                       $model: "",
                       $error: false
                   }
                },
                type: Object
            },
            inputType: {
                type: String,
                default: "textarea",
                validator: function (value) {
                    return [
                        'textarea',
                        'checkbox',
                        'time',
                        "buttons",
                    ].indexOf(value) !== -1;
                }
            },
            labelText: String,
            exampleText: String,
            warningText: String,
            boxes: Array,
            rows: {
                type: Number,
                default: 1
            },
            storeCommit: String,
        },
        methods: {
            updateStore(payload) {
                this.$store.commit(this.storeCommit, payload);
            }
        },
        data: function () {
            return {
                id: null,
                text: "",
                checked: "",
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>

<template>
    <div class="form-group row labelled-textarea">
        <label :for="'textarea' + id"> <b v-if="isOptional">
            Optional:</b> {{ labelText }} <br />
            <span v-if="subLabel" class="text-muted"> {{ subLabel}} </span>
        </label>
        <textarea :id="'textarea' + id" class="form-control form-control-lg col-12"> </textarea>
        <span>{{ numCharacters }} characters left</span>
    </div>
</template>

<script>
    export default {
        props: {
            labelText: String,
            subLabel: String,
            isOptional: Boolean,
        },
        data: function () {
            return {
                id: null,
                isOptional: true,
                numCharacters: 100,
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>

<template>
    <div class="form-group row labelled-textarea">
        <label :for="id"> <b v-if="isOptional">Optional:</b> {{ label_text }}
        <br />
        <span :for="id" v-if="moreInfo" class="text-muted"> {{ sub_label}} </span>
        </label>
        <textarea :id="id" class="form-control form-control-lg col-12"> </textarea>
        <span>{{ num_characters }} characters left</span>
    </div>
</template>

<script>
    export default {
        data: function () {
            return {
                label_text: "test text",
                sub_label: "test sub",
                moreInfo: true,
                id: null,
                isOptional: true,
                num_characters: 100,
            }
        },
        mounted: function () {
            this.id = this._uid;
        }
    }
</script>

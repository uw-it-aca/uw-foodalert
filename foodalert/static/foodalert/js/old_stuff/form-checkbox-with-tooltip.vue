<template>
    <div>
        <b-form-checkbox
         :v-model="modelt"
         :key="keyt"
         :value="valuet"
         :disabled="disabledt">
            <slot name="checkbox-text"></slot>
            <a href="#" v-on:click.stop="toggleTooltip()">
                <slot name="tooltip-link-text"></slot>
            </a>
        </b-form-checkbox>
        <div class="custom-tooltip" v-if="showTooltip">
            <slot name="tooltip-text"></slot>
        </div>
    </div>
</template>

<script type="text/javascript">
  export default {
    methods: {
        toggleTooltip() {
            this.showTooltip = !this.showTooltip;
        },
        renderTooltip() {
            return this.showTooltip;
        }
    },
    props: ['modelt', 'keyt', 'valuet', 'disabledt'],
    data() {
      return {
        showTooltip: false,
      }
    }
  }
</script>

<style>
    .custom-tooltip {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #e9e9e9;
        color: #707070;
    }
</style>

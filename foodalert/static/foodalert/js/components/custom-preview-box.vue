<template>
    <div class="custom-preview-box">
      <slot>
        <h1>Hello this will be content</h1>
      </slot>
    </div>
</template>

<script type="text/javascript">
export default {
};
</script>

<style>
    .custom-preview-box {
        border-radius: 18px 18px 18px 18px;
        background-color: #F1F0F0;
        color: #484848;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>

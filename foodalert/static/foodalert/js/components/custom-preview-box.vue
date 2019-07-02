<template>
    <div class="custom-preview-box">
      <slot>
        <h1>Hello this will be content</h1>
      </slot>
    </div>
</template>

<script type="text/javascript">
  export default {
  }
</script>

<style>
    .custom-preview-box {
        border-radius: 18px 18px 6px 18px;
        background-color: #e9e9e9;
        color: #707070;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>

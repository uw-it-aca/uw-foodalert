<template>
    <b-collapse :id="bid" class="custom-collapse collapse-text-box">
        <div class="custom-text-box">
            <slot>
                <h1>Hello this will be content</h1>
            </slot>
        </div>
    </b-collapse>
</template>

<script type="text/javascript">
  export default {
      props: {
          bid: String,
      }
  }
</script>

<style>
    .collapse-text-box .custom-text-box {
        border-radius: 10px 10px 10px 10px;
        background-color: #F1F0F0;
        color: #484848;
        padding: 1rem;
        margin-top: 10px;
    }
</style>

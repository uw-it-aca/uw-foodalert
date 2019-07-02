<template>
    <b-collapse :id="bid">
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
    .custom-text-box {
        border-radius: 10px 10px 10px 10px;
        background-color: #e9e9e9;
        color: #707070;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>

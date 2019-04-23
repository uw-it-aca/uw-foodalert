<template>
  <b-container style="padding: 40px 15px;">
        <b-row align-self="center" align-h="center">
            <img src="../../img/hungryhusky.png">
        </b-row>
        <br>
        <b-row align-self="center" align-h="center">
            <h1>404 Not Found</h1>
        </b-row>
        <br>
        <b-row align-self="center" align-h="center">
            <h2>The Page You Requested Could Not Be Found</h2>
        </b-row>
        <br>
        <b-row align-self="center" align-h="center">
            <b-link to="/">
                <button type="button" class="btn btn-outline-primary">
                    Go To Homepage
                </button>
            </b-link>
        </b-row>
  </b-container>
</template>

<script type="text/javascript">
  export default {
  }
</script>

<style>
    .btn-outline-primary:hover, .btn-outline-primary:active, .btn-outline-primary:visited {
        background-color: #4b2e83 !important;
    }
    .btn-outline-primary {
        border-color: #4b2e83 !important;
    }
</style>

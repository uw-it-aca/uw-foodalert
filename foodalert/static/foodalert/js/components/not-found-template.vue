<template>
  <main>
    <b-container style="padding: 40px 15px;">
          <b-row align-self="center" align-h="center">
              <img src="../../img/hungryhusky.png" alt="Hungry Husky logo">
          </b-row>
          <br>
          <b-row align-self="center" align-h="center">
              <h1>404 Not Found</h1>
          </b-row>
          <br>
          <b-row align-self="center" align-h="center">
              <h2 class="h2">The Page You Requested Could Not Be Found</h2>
          </b-row>
          <br>
          <b-row align-self="center" align-h="center">
              <button class="btn btn-outline-primary"
                      href="#"
                      @click="goHome()"
                      @keyDown="goHome()">
                  Go To Homepage
              </button>
          </b-row>
    </b-container>
  </main>
</template>

<script type="text/javascript">
export default {
  methods: {
    goHome() {
      this.$router.push('/');
    },
  },
};
</script>

<style>
    .btn:hover.btn-outline-primary:hover,
    .btn:active.btn-outline-primary:active,
    .btn:visited.btn-outline-primary:visited {
        background-color: #4b2e83;
        border-color: #4b2e83;
    }
    .btn.btn-outline-primary {
        border-color: #4b2e83;
    }
</style>

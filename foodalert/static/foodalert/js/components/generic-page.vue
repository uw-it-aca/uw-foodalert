<template>
  <div class="page">
    <div class="page-content pb-2">
      <alert-box v-if="notificationState" aria-live="polite" role="alert">
          <slot name="notification"></slot>
      </alert-box>
      <header class="md-5 mb-2" role="banner">
        <b-navbar class="mx-auto" style="height: 64px; max-width: 1232px;">
          <b-navbar-brand class="pl-2 pb-2">
            <img :src="require('../../img/food-alert-logo.svg')"
                  alt="UW Food Alert Logo" height="22"
                  >
          </b-navbar-brand>
          <b-navbar-nav class="d-flex d-sm-none ml-auto">
            <b-nav-item-dropdown variant="link" :text="netID"
              right toggle-class="text-decoration-none">
              <b-dropdown-item href="#">Sign out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
          <b-navbar-nav class="d-none d-sm-flex ml-auto">
            <b-nav-form>
              <label for="sign-out">
                {{netID}}
                <b-button variant="link"
                  id="sign-out"
                  type="submit">
                  Sign out
                </b-button>
              </label>
            </b-nav-form>
          </b-navbar-nav>
        </b-navbar>
      </header>
      <main id="page-loader" v-if="showUpdateOverlay">
        <div>
          <b-spinner label="Loading..."></b-spinner>
        </div>
      </main>
      <main id="standard-body" class="standard-container mt-md-5 mt-3" v-show="!showUpdateOverlay">
        <h1 id="standard-heading">
            <slot name="heading"></slot>
        </h1>
        <slot name="body"></slot>
        <slot name="navigation"></slot>
      </main>
    </div>
    <footer id="relative-footer" class="text-center" role="contentinfo">
      <a href="mailto:help@uw.edu?subject=Hungry Husky support">
        Contact support
      </a>
      <p>© 2019 University of Washington</p>
    </footer>
  </div>
</template>

<script>
import AlertBox from '../components/alert-box.vue';
export default {
  components: {
    'alert-box': AlertBox,
  },
  props: {
    startWithNotification: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      notificationState: false,
      showUpdateOverlay: false,
    };
  },
  beforeMount() {
    if (this.startWithNotification) {
      this.notificationState = true;
    }
  },
  mounted() {
    this.$nextTick(
        function() {
          document.activeElement.blur();
          const newFocus = document.querySelector('h1');

          newFocus.setAttribute('tabindex', '-1');
          newFocus.style.outline = 'none';
          newFocus.focus();
          newFocus.removeAttribute('tabindex');

          window.addEventListener('resize', this.updateHeightOfPage);
          this.updateHeightOfPage();
        }.bind(this)
    );
  },
  methods: {
    updateHeightOfPage() {
      document.querySelector('.page').style.minHeight =
        window.innerHeight + 'px';
    },
  },
};
</script>

<style>
    header {
      border-bottom: 1px solid #ebebeb;
    }
    #standard-notification {
        height: 0;
        overflow: visible;
        position: fixed;
        width: 100%;
        z-index: 1;
    }
    #standard-heading {
        font-size: 32px;
        line-height: 1.2;
        font-weight: 700;
        color: #484848;
        -moz-osx-font-smoothing: grayscale;
    }
    #standard-body {
        font-size:16px;
        line-height: 1.5;
        font-weight: 400;
        color: #484848;
        -moz-osx-font-smoothing: grayscale;
    }

    #page-loader {
      flex-grow: 1;
      display: flex;
    }

    #page-loader > div {
      margin: auto;
      font-size: 25px;
    }

    #page-loader > div > span {
      width: 100px;
      height: 100px;
    }

    .page .page-content .page-content-padding {
      padding-left: 24px;
      padding-right: 24px;
      padding-bottom: 8px;
    }

    .page .page-content {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
    }

    .page {
        display: flex;
        min-height: 100vh;
        flex-direction: column;
        align-content: space-between;
    }

    #relative-footer {
        margin-top: auto;
        padding-top: 16px;
        font-size: 12px;
        width: 100%;
        -moz-osx-font-smoothing: grayscale;
    }

    .standard-container {
      max-width: 700px;
      padding-left: 24px;
      padding-right: 24px;
      position: relative;
      margin-left: auto;
      margin-right: auto;
    }

    .foodalert .alert {
      font-weight: 600;
      font-size: 20px;
      background-color: #3d9970;
      color: white;
      display: flex;
      align-items: center;
      height: 70px;
      border-radius: 10px;
    }

    .foodalert .alert-dismissible .close{
      height: 100%;
      opacity: 1;
    }

    .foodalert .alert-dismissible .close:hover{
      color: white;
    }

    .foodalert .btn.btn-link[role='link'] {
      vertical-align: initial;
    }
</style>

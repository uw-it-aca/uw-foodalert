<template>
  <div class="page">
    <div class="page-content pb-2">
      <header class="md-5 mb-2">
        <slot name="banner"></slot>
        <div class="standard-container">
          <alert-box v-if="notificationState">
            <slot name="notification"></slot>
          </alert-box>
          <h1 id="standard-heading" class="mt-4">
            <slot name="heading"></slot>
          </h1>
        </div>
      </header>
      <main id="standard-body" class="standard-container">
        <slot name="body"></slot>
        <slot name="navigation"></slot>
      </main>
    </div>
    <footer id="relative-footer" class="text-center">
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
    };
  },
  beforeMount() {
    if (this.startWithNotification) {
      this.notificationState = true;
    }
  },
  mounted() {
    document.activeElement.blur();
    let newFocus = document.querySelector('h1');
    newFocus.setAttribute("tabindex", "-1");
    newFocus.style.outline = "none";
    newFocus.focus();
    newFocus.removeAttribute("tabindex")
  },
};
</script>

<style>
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

    .page .page-content .page-content-padding {
      padding-left: 24px;
      padding-right: 24px;
      padding-bottom: 8px;
    }

    .page {
        display: flex;
        min-height: 100vh;
        flex-direction: column;
        align-content: space-between;
    }

    #relative-footer {
        margin-top: auto;
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
</style>

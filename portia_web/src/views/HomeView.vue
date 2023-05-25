<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <!-- <TheWelcome /> -->
    
        
    

      <div class="social">
        <div class="row">
          {% if associated.get('google-oauth2') %}
              <form id="google-oauth2-disconnect"
                      class="disconnect-form col-md-2"
                      action="/disconnect/google-oauth2/"
                      method="post">
                  <input type="hidden" name="csrfmiddlewaretoken" value="">
                  <a class="btn btn-danger" name="google oauth2" href="#">
                  <i class="fa-brands fa-google"></i>
                  Disconnect Google OAuth2
                  </a>
              </form>
          {% else %}
              <a id="google-oauth2-button"
                  class="col-md-2 btn btn-light"
                  name="google oauth2"
                  href="/login/google-oauth2/">
                  <i class="fa-brands fa-google"></i>
              Google OAuth2
              </a>
          {% endif %}

          <a id="google-oauth2-button"
                  class="col-md-2 btn btn-light"
                  name="google oauth2"
                  href="http://localhost:5000/login/google-oauth2/">
                  <i class="fa-brands fa-google"></i>
              Google OAuth2
              </a>
        </div>
      </div>

      <div>
        <a class="btn btn-primary" href="http://127.0.0.1:5000/logout/" id="logout">
          <i class="fa fa-sign-out"></i>
          Logout
        </a>
      </div>
  </main>
</template>

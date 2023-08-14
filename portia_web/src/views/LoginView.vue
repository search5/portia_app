<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";
import NounAvartar from "../components/icons/NounAvartar.vue";

export default defineComponent({
  name: "LoginView",
  components: {NounAvartar, FooterView, TopMenuView},
  data: () => ({
    input_data: {
      email: '',
      password: ''
    }
  }),
  methods: {
    login () {
      // TODO
    }
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="container">
      <div class="row">
        <div class="col-12">
  <!--            {% with messages = get_flashed_messages() %}-->
  <!--                {% if messages %}-->
  <!--                <div class="alert alert-danger mt-3" role="alert"></div>-->
  <!--                <ul class=flashes>-->
  <!--                {% for message in messages %}-->
  <!--                    <li>{{ message }}</li>-->
  <!--                {% endfor %}-->
  <!--                </ul>-->
  <!--                </div>-->
  <!--                {% endif %}-->
  <!--            {% endwith %}-->

          <div class="login-form">
            <h2 class="text-center">Member Login</h2>
            <form>
              <div class="avatar">
                <NounAvartar />
              </div>
              <div class="mb-3">
                <input type="text" class="form-control" name="email" placeholder="Username" required="required" v-model="input_data.email">
              </div>
              <div class="mb-3">
                <input type="password" class="form-control" name="password" placeholder="Password" required="required" v-model="input_data.password">
              </div>
              <div class="mb-3 clearfix">
                <button type="button" class="btn btn-primary fa-pull-right" @click="login">로그인 하기</button>
              </div>
            </form>
            <div class="hint-text">계정이 없으면 가입하시겠어요? <RouterLink :to="{name: 'portia_join'}">가입하러 가기</RouterLink></div>
          </div>
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>
.form-control {
  background: #f2f2f2;
  font-size: 16px;
  border-color: transparent;
  box-shadow: none !important;
}

.form-control:focus {
  border-color: #91d5a8;
  background: #e9f5ee;
}

.form-control, .btn {
  border-radius: 2px;
}

.login-form {
  width: 380px;
  margin: 0 auto;
}

.login-form h2 {
  margin: 0;
  padding: 30px 0;
  font-size: 34px;
}

.login-form .avatar {
  margin: 0 auto 30px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  z-index: 9;
  background: #4aba70;
  padding: 15px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
}

.login-form form {
  color: #7a7a7a;
  border-radius: 4px;
  margin-bottom: 20px;
  background: #fff;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
  padding: 30px;
}

.login-form .btn {
  font-size: 16px;
  line-height: 26px;
  min-width: 120px;
  font-weight: bold;
  background: #4aba70;
  border: none;
}

.login-form .btn:hover, .login-form .btn:focus{
  background: #40aa65;
  outline: none !important;
}

.login-form a {
  color: #4aba70;
}

.login-form a:hover {
  text-decoration: underline;
}
</style>
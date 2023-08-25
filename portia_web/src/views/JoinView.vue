<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";
import { Toast } from 'bootstrap';
import {every} from "lodash-es";
import axios from "axios";

let toastBootstrap = null

export default defineComponent({
  name: "JoinView",
  components: {FooterView, TopMenuView},
  data: () => ({
    input_data: {
      real_name: '',
      real_email: '',
      user_password: '',
      post_code: '',
      addresses: '',
      detail_address: ''
    }
  }),
  methods: {
    join () {
      if (!every(this.input_data)) {
        toastBootstrap.show()
        return false
      }

      axios.post('/api/users/join', this.input_data).then(resp => {
        console.log(resp)
      }).catch(error => {
        toastBootstrap.show()
      })
    }
  },
  mounted () {
    toastBootstrap = Toast.getOrCreateInstance(this.$refs.liveToast)
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <div class="toast-container position-fixed top-0 start-0 p-3">
      <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true" ref="liveToast">
        <div class="toast-header">
          <svg class="bd-placeholder-img rounded me-2" width="20" height="20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice" focusable="false">
            <rect width="100%" height="100%" fill="#007aff"/>
          </svg>
          <strong class="me-auto">Portia Shop</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          회원 가입에 실패했습니다.
        </div>
      </div>
    </div>

    <div class="container">
      <div class="row mt-4 mb-4">
        <div class="col-12">
          <h4>회원 가입하기</h4>
          <form>
            <div class="row">
              <div class="mb-3 col-md-2">
                <label for="inputName">이름</label>
                <input type="text" class="form-control" id="inputName" v-model="input_data.real_name">
              </div>
              <div class="mb-3 col-md-4">
                <label for="inputEmail">Email</label>
                <input type="email" class="form-control" id="inputEmail" v-model="input_data.real_email">
              </div>
              <div class="mb-3 col-md-6">
                <label for="inputPassword">비밀번호</label>
                <input type="password" class="form-control" id="inputPassword" v-model="input_data.user_password">
              </div>
            </div>
            <div class="row">
              <div class="mb-3 col-md-2">
                <label for="inputPostCode">우편번호</label>
                <input type="text" class="form-control" id="inputPostCode" v-model="input_data.post_code">
              </div>
              <div class="mb-3 col-md-10">
                <label for="inputAddress">주소</label>
                <input type="text" class="form-control" id="inputAddress" v-model="input_data.addresses">
              </div>
            </div>
            <div class="mb-3">
              <label for="inputAddress2">상세 주소</label>
              <input type="text" class="form-control" id="inputAddress2" v-model="input_data.detail_address">
            </div>

            <button type="button" @click="join" class="btn btn-primary">가입하기</button>
          </form>
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>
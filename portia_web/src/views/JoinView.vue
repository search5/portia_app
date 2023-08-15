<script>
import {defineComponent} from 'vue'
import TopMenuView from "../components/TopMenuView.vue";
import FooterView from "../components/FooterView.vue";

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
      // TODO
    }
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>
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
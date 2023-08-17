<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";

export default defineComponent({
  name: "MyInfoView",
  components: {TopMenuView, FooterView},
  data: () => ({
    input_data: {
      real_name: '홍길동',
      real_email: 'gdhong@knou.ac.kr',
      user_current_password: '',
      user_new_password: '',
      user_new_password_confirm: '',
      post_code: '',
      addresses: '',
      detail_address: ''
    }
  }),
  methods: {
    modify () {
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
          <h4>내 정보</h4>
          <form>
            <div class="row">
              <div class="mb-3 col-md-2">
                <label for="inputName">이름</label>
                <input type="text" class="form-control form-control-plaintext" readonly id="inputName" v-model="input_data.real_name">
              </div>
              <div class="mb-3 col-md-4">
                <label for="inputEmail">Email</label>
                <input type="email" class="form-control form-control-plaintext" readonly id="inputEmail" v-model="input_data.real_email">
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

            <hr>
            <h5 class="float-start">비밀번호 변경</h5>
            <span class="small text-danger clearfix">(비밀번호를 변경하실 때만 입력하세요)</span>
            <div class="row">
              <div class="mb-3 col-md-6">
                <label for="inputCurrentPassword">현재 비밀번호</label>
                <input type="password" class="form-control" id="inputCurrentPassword" v-model="input_data.user_current_password">
              </div>
            </div>
            <div class="row">
              <div class="mb-3 col-md-6">
                <label for="inputNewPassword">새 비밀번호</label>
                <input type="password" class="form-control" id="inputNewPassword" v-model="input_data.user_new_password">
              </div>
              <div class="mb-3 col-md-6">
                <label for="inputNewPasswordConfirm">새 비밀번호 확인</label>
                <input type="password" class="form-control" id="inputNewPasswordConfirm" v-model="input_data.user_new_password_confirm">
              </div>
            </div>

            <button type="button" @click="modify" class="btn btn-primary">정보 수정</button>
          </form>
        </div>
      </div>
    </div>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>
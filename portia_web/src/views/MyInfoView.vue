<script>
import {defineComponent} from 'vue'
import FooterView from "@/components/FooterView.vue";
import TopMenuView from "@/components/TopMenuView.vue";
import MyPageSlot from "../components/MyPageSlot.vue";
import {http_inst} from "../lib";

export default defineComponent({
  name: "MyInfoView",
  components: {MyPageSlot, TopMenuView, FooterView},
  data: () => ({
    input_data: {
      real_name: '',
      real_email: '',
      real_phone: '',
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
      let send_data = {
        real_name: this.input_data.real_name,
        real_email: this.input_data.real_email,
        real_phone: this.input_data.real_phone,
        post_code: this.input_data.post_code,
        addresses: this.input_data.addresses,
        detail_address: this.input_data.detail_address
      }

      // 현재 비밀번호 입력 시
      if (this.input_data.user_current_password !== '') {
        Object.assign(send_data, {
          user_current_password: this.input_data.user_current_password,
          user_new_password: this.input_data.user_new_password,
          user_new_password_confirm: this.input_data.user_new_password_confirm
        })
      }

      http_inst.put('/api/myinfo', send_data).then(result => {
        alert('사용자 정보가 수정되었습니다')
      }).catch(error => {
        alert('사용자 정보 수정에 실패했습니다')
      })
    }
  },
  mounted() {
    http_inst.get('/api/myinfo').then(result => {
      const myinfo = result.data
      Object.assign(this.input_data, myinfo)
    }).catch(error => {
      alert('내 정보를 읽어오는데 실패했습니다')
    })
  }
})
</script>

<template>
  <div>
    <TopMenuView></TopMenuView>

    <MyPageSlot>
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
              <div class="mb-3 col-md-6">
                <label for="inputPhone">휴대전화</label>
                <input type="text" class="form-control" id="inputPhone" v-model="input_data.real_phone">
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
    </MyPageSlot>>

    <FooterView></FooterView>
  </div>
</template>

<style scoped>

</style>
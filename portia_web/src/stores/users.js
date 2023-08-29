import {defineStore} from "pinia";
import {every} from "lodash-es";
import axios from "axios";

export const useUsersStore = defineStore('users', {
  state: () => ({
    api: ''
  }),
  getters: {
  },
  actions: {
    is_login: () => localStorage.getItem('access_token') !== null,
    login_action (input_data) {
      if (!every(input_data)) {
        alert('ID 또는 비밀번호가 입력되지 않았습니다')
        return false
      }

      return new Promise((resolve, reject) => {
        axios.patch('/api/login', input_data).then(result => {
          localStorage.setItem('access_token', result.data.access_token)
          localStorage.setItem('refresh_token', result.data.refresh_token)
          localStorage.setItem('username', result.data.username)

          resolve({success: true})
        }).catch(result => {
          reject({success: false})
        })
      })
    }
  }
})
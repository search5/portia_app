import './scss/styles.scss'

// Import all of Bootstrap's JS
// import * as bootstrap from 'bootstrap'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import {
  faShoppingCart,
  faTrash,
  faCheck,
  faUser,
  faTruck,
  faBox,
  faChevronLeft
} from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faShoppingCart, faTrash, faCheck, faUser, faTruck, faBox, faChevronLeft)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
